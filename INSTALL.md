# Installation Guide

## Quick Install (Recommended)

Install the DevContainer CLI directly from GitHub:

```bash
# Download and install
curl -fsSL https://raw.githubusercontent.com/ivikasavnish/devcontainers/main/devcontainer-cli -o /usr/local/bin/devcontainer
chmod +x /usr/local/bin/devcontainer

# Verify installation
devcontainer --version
```

## Manual Installation

### Option 1: Clone the repository

```bash
# Clone the repo
git clone https://github.com/ivikasavnish/devcontainers.git
cd devcontainers

# Make scripts executable
chmod +x devcontainer-cli setup-devcontainer.sh auto-detect.sh

# Add to PATH (add to your ~/.bashrc or ~/.zshrc)
export PATH="$PATH:/path/to/devcontainers"
```

### Option 2: Download standalone CLI

The CLI will automatically fetch templates from GitHub when needed:

```bash
# Download CLI only
curl -O https://raw.githubusercontent.com/ivikasavnish/devcontainers/main/devcontainer-cli
chmod +x devcontainer-cli

# Move to PATH
sudo mv devcontainer-cli /usr/local/bin/devcontainer
```

## Usage

Once installed, use the CLI from anywhere:

```bash
# Auto-detect and setup
devcontainer auto /path/to/project

# Install specific stack
devcontainer install rails /path/to/project

# List available stacks
devcontainer list

# Get help
devcontainer --help
```

## Requirements

- **Docker Desktop** or **Docker Engine** with Docker Compose
- **VS Code** with Dev Containers extension
- **Git** (for cloning)
- **curl** (for remote fetching)
- Python 3 (optional, for advanced builder features)

## Uninstall

```bash
# If installed to /usr/local/bin
sudo rm /usr/local/bin/devcontainer

# If cloned
rm -rf /path/to/devcontainers
# Remove from PATH in ~/.bashrc or ~/.zshrc
```

## Updates

```bash
# If cloned
cd devcontainers
git pull origin main

# If standalone
curl -fsSL https://raw.githubusercontent.com/ivikasavnish/devcontainers/main/devcontainer-cli -o /usr/local/bin/devcontainer
chmod +x /usr/local/bin/devcontainer
```
