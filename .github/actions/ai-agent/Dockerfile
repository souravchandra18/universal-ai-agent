# Base image with Python 3.11
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    npm \
    ruby-full \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

# Install JS analyzer
RUN npm install -g eslint

# Install Ruby analyzers
RUN gem install --user-install rubocop brakeman
ENV PATH="$PATH:$(ruby -e 'puts Gem.user_dir')/bin"

# Install Trivy
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Install tfsec
RUN curl -sSfL https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash
ENV PATH="$PATH:$HOME/.tfsec/bin"

# Copy the action code
COPY .github/actions/ai-agent /app
WORKDIR /app

# Set entrypoint
ENTRYPOINT ["python", "main.py"]
