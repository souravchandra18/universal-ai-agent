import os
from analyzers import detect_languages_and_tools, run_analyzers
from llm import call_llm
from github import Github, Auth
import json

def run_agent():
    # Read environment variables
    llm_provider = os.getenv('INPUT_LLM_PROVIDER', 'openai')
    run_semgrep = os.getenv('INPUT_RUN_SEMGREP', 'true').lower() == 'true'
    github_token = os.getenv('GITHUB_TOKEN')  # ✅ using GITHUB_TOKEN

    repo_root = os.getenv('GITHUB_WORKSPACE', os.getcwd())
    print(f"Repo root: {repo_root}")

    # Detect languages and tools
    detected = detect_languages_and_tools(repo_root)
    print(f"Detected languages/tools: {detected}")

    # Run analyzers
    analyzer_results = run_analyzers(repo_root, detected, run_semgrep)

    # Build prompt for LLM
    prompt = build_prompt(detected, analyzer_results)
    llm_response = call_llm(provider=llm_provider, prompt=prompt)

    # Post PR comment only (skip check runs)
    event_name = os.getenv('GITHUB_EVENT_NAME', '')
    event_path = os.getenv('GITHUB_EVENT_PATH', '')

    if github_token and os.getenv('GITHUB_REPOSITORY') and 'pull_request' in event_name and event_path:
        g = Github(auth=Auth.Token(github_token))
        repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

        try:
            # Load event payload JSON to get PR number
            with open(event_path, 'r') as f:
                event = json.load(f)
            pr_number = event['pull_request']['number']  # ✅ safe extraction
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(
                llm_response.get('summary', 'AI Agent completed analysis')
            )
            print(f"Posted AI Agent summary as PR comment on PR #{pr_number}.")
        except Exception as e:
            print(f"Failed to post PR comment: {e}")

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
