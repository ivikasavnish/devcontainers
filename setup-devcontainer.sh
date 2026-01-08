#!/bin/bash
# Quick setup script for devcontainers
# Usage: ./setup-devcontainer.sh <stack> <target-directory>
# Example: ./setup-devcontainer.sh rails ~/my-rails-project

set -e

STACK=$1
TARGET=$2
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_URL="https://github.com/ivikasavnish/devcontainers"
USE_REMOTE=false

# Check if templates exist locally, otherwise use remote
if [ ! -d "$SCRIPT_DIR/$STACK" ]; then
    USE_REMOTE=true
fi

if [ -z "$STACK" ] || [ -z "$TARGET" ]; then
    echo "Usage: $0 <stack> <target-directory>"
    echo ""
    echo "Available stacks:"
    echo "  rails        - Ruby on Rails + PostgreSQL + Redis"
    echo "  strapi       - Strapi CMS + PostgreSQL"
    echo "  go-react     - Go + React + PostgreSQL + Redis"
    echo "  rails-react  - Rails API + React + PostgreSQL + Redis"
    echo "  python       - Python + PostgreSQL + Redis"
    echo ""
    echo "Example: $0 rails ~/my-rails-project"
    exit 1
fi

if [ "$USE_REMOTE" = true ]; then
    echo "📦 Fetching templates from GitHub..."
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR" EXIT
    
    if ! curl -sL "$REPO_URL/archive/refs/heads/main.tar.gz" | tar xz -C "$TEMP_DIR"; then
        echo "Error: Failed to download templates from $REPO_URL"
        exit 1
    fi
    
    SCRIPT_DIR="$TEMP_DIR/devcontainers-main"
    
    if [ ! -d "$SCRIPT_DIR/$STACK" ]; then
        echo "Error: Stack '$STACK' not found!"
        echo "Available stacks: rails, strapi, go-react, rails-react, python"
        exit 1
    fi
elif [ ! -d "$SCRIPT_DIR/$STACK" ]; then
    echo "Error: Stack '$STACK' not found!"
    echo "Available stacks: rails, strapi, go-react, rails-react, python"
    exit 1
fi

if [ ! -d "$TARGET" ]; then
    echo "Error: Target directory '$TARGET' does not exist!"
    exit 1
fi

if [ -d "$TARGET/.devcontainer" ]; then
    echo "Warning: .devcontainer already exists in $TARGET"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
    rm -rf "$TARGET/.devcontainer"
fi

echo "Setting up $STACK devcontainer in $TARGET..."
cp -r "$SCRIPT_DIR/$STACK/.devcontainer" "$TARGET/"
echo "✓ Copied devcontainer configuration"

if [ -f "$SCRIPT_DIR/$STACK/README.md" ]; then
    cp "$SCRIPT_DIR/$STACK/README.md" "$TARGET/DEVCONTAINER.md"
    echo "✓ Copied documentation to DEVCONTAINER.md"
fi

echo ""
echo "Setup complete! 🎉"
echo ""
echo "Next steps:"
echo "1. Open $TARGET in VS Code"
echo "2. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux)"
echo "3. Select 'Dev Containers: Reopen in Container'"
echo "4. Wait for container to build and dependencies to install"
echo ""
echo "Documentation: $TARGET/DEVCONTAINER.md"
