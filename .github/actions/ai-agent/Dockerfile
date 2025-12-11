# Base image with Python 3.11
FROM python:3.11-slim

# Install system dependencies + OpenJDK 11
RUN apt-get update && apt-get install -y \
    curl \
    git \
    npm \
    ruby-full \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /tmp/requirements.txt

# Install JS analyzer
RUN npm install -g eslint

# Install Ruby analyzers
RUN gem install --user-install rubocop brakeman
ENV PATH="$PATH:/root/.gem/ruby/3.2.0/bin"

# Install Trivy
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Install tfsec
RUN curl -sSfL https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash
ENV PATH="$PATH:/root/.tfsec/bin"

# Copy the action code
COPY . /app
WORKDIR /app

# Entrypoint
ENTRYPOINT ["python3", "main.py"]
