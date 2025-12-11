import os
from analyzers import detect_languages_and_tools, run_analyzers
from llm import call_llm
from github import Github, Auth
import json

def run_agent():
    llm_provider = os.getenv('INPUT_LLM_PROVIDER', 'openai')
    run_semgrep = os.getenv('INPUT_RUN_SEMGREP', 'true').lower() == 'true'
    github_token = os.getenv('VAULT_TOKEN')

    repo_root = os.getenv('GITHUB_WORKSPACE', os.getcwd())
    print(f"Repo root: {repo_root}")

    detected = detect_languages_and_tools(repo_root)
    print(f"Detected languages/tools: {detected}")

    analyzer_results = run_analyzers(repo_root, detected, run_semgrep)

    prompt = build_prompt(detected, analyzer_results)
    llm_response = call_llm(provider=llm_provider, prompt=prompt)

    if github_token and os.getenv('GITHUB_REPOSITORY') and os.getenv('GITHUB_SHA'):
        #g = Github(github_token)
        g = Github(auth=Auth.Token(github_token))
        repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
        sha = os.getenv('GITHUB_SHA')

        # Create a check run
        repo.create_check_run(
            name='AI Universal Agent',
            head_sha=sha,
            status='completed',
            conclusion='neutral',
            output={
                'title': 'AI Agent Report',
                'summary': llm_response.get('summary', 'See details'),
                'text': llm_response.get('full', json.dumps(analyzer_results, indent=2))
            }
        )

        # Post PR comment if applicable
        event_name = os.getenv('GITHUB_EVENT_NAME', '')
        if 'pull_request' in event_name:
            ref = os.getenv('GITHUB_REF', '')
            pr_number = int(ref.split('/')[-1])
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(llm_response.get('summary', 'AI Agent completed analysis'))

    print('AI Agent finished.')

def build_prompt(detected, analyzer_results):
    prompt = (
        "You are an expert engineering reviewer. Produce:\n"
        "1) A short summary of the repo health (code quality, security, reliability).\n"
        "2) A prioritized list of 6 actionable items with severity, suggested fix, and commands.\n"
        "3) Line-level suggestions if analyzer outputs indicate file/line numbers.\n"
        f"Repository analysis data:\n{json.dumps(analyzer_results, indent=2)}"
    )
    return prompt

if __name__ == '__main__':
    run_agent()
