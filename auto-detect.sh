#!/bin/bash
# Auto-detect project type and recommend devcontainer
# Usage: ./auto-detect.sh <project-directory>

set -e

PROJECT_DIR="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Directory '$PROJECT_DIR' does not exist!"
    exit 1
fi

cd "$PROJECT_DIR"
PROJECT_DIR="$(pwd)"

echo "🔍 Analyzing project: $PROJECT_DIR"
echo ""

# Detection logic
DETECTED_STACK=""
CONFIDENCE="unknown"
DETAILS=()

# Check for Rails
if [ -f "Gemfile" ] && grep -q "rails" Gemfile 2>/dev/null; then
    if [ -d "frontend" ] || [ -f "frontend/package.json" ]; then
        DETECTED_STACK="rails-react"
        CONFIDENCE="high"
        DETAILS+=("✓ Found Gemfile with Rails")
        DETAILS+=("✓ Found frontend/ directory")
    else
        DETECTED_STACK="rails"
        CONFIDENCE="high"
        DETAILS+=("✓ Found Gemfile with Rails")
    fi
fi

# Check for Strapi
if [ -f "package.json" ] && grep -q "strapi" package.json 2>/dev/null; then
    DETECTED_STACK="strapi"
    CONFIDENCE="high"
    DETAILS+=("✓ Found package.json with Strapi")
fi

# Check for Go + React
if [ -f "go.mod" ] && [ -d "backend" ] && [ -d "frontend" ]; then
    DETECTED_STACK="go-react"
    CONFIDENCE="high"
    DETAILS+=("✓ Found go.mod")
    DETAILS+=("✓ Found backend/ and frontend/ directories")
elif [ -f "backend/go.mod" ] && [ -f "frontend/package.json" ]; then
    DETECTED_STACK="go-react"
    CONFIDENCE="high"
    DETAILS+=("✓ Found backend/go.mod")
    DETAILS+=("✓ Found frontend/package.json")
fi

# Check for Python projects
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    if grep -q "fastapi\|django\|flask" requirements.txt 2>/dev/null || \
       grep -q "fastapi\|django\|flask" pyproject.toml 2>/dev/null; then
        DETECTED_STACK="python"
        CONFIDENCE="high"
        DETAILS+=("✓ Found Python web framework")
    elif [ -z "$DETECTED_STACK" ]; then
        DETECTED_STACK="python"
        CONFIDENCE="medium"
        DETAILS+=("✓ Found Python project files")
    fi
fi

# Check for plain Go project
if [ -f "go.mod" ] && [ -z "$DETECTED_STACK" ]; then
    DETECTED_STACK="go-react"
    CONFIDENCE="medium"
    DETAILS+=("✓ Found go.mod (assuming API project)")
fi

# Check for plain Node.js project
if [ -f "package.json" ] && [ -z "$DETECTED_STACK" ]; then
    DETECTED_STACK="strapi"
    CONFIDENCE="low"
    DETAILS+=("? Found package.json (Node.js project)")
fi

# Display results
echo "📊 Detection Results:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for detail in "${DETAILS[@]}"; do
    echo "   $detail"
done
echo ""

if [ -z "$DETECTED_STACK" ]; then
    echo "❌ Could not detect project type!"
    echo ""
    echo "💡 Available stacks:"
    echo "   • rails        - Ruby on Rails"
    echo "   • strapi       - Strapi CMS"
    echo "   • go-react     - Go + React"
    echo "   • rails-react  - Rails API + React"
    echo "   • python       - Python (FastAPI/Django/Flask)"
    echo ""
    echo "Usage: $SCRIPT_DIR/setup-devcontainer.sh <stack> $PROJECT_DIR"
    exit 1
fi

# Display recommendation
case $CONFIDENCE in
    high)
        echo "✅ Recommended stack: $DETECTED_STACK (confidence: $CONFIDENCE)"
        ;;
    medium)
        echo "⚠️  Suggested stack: $DETECTED_STACK (confidence: $CONFIDENCE)"
        ;;
    low)
        echo "❓ Possible stack: $DETECTED_STACK (confidence: $CONFIDENCE)"
        ;;
esac

echo ""
echo "📋 Stack Details:"
case $DETECTED_STACK in
    rails)
        echo "   Languages: Ruby 3.3 + Rails"
        echo "   Database: PostgreSQL 16"
        echo "   Cache: Redis 7"
        echo "   Ports: 3000 (Rails), 5432 (PostgreSQL)"
        ;;
    strapi)
        echo "   Languages: Node.js 20"
        echo "   Framework: Strapi CMS"
        echo "   Database: PostgreSQL 16"
        echo "   Ports: 1337 (Strapi), 5432 (PostgreSQL)"
        ;;
    go-react)
        echo "   Languages: Go 1.22 + Node.js 20"
        echo "   Database: PostgreSQL 16"
        echo "   Cache: Redis 7"
        echo "   Ports: 8080 (Go API), 3000 (React), 5432 (PostgreSQL)"
        ;;
    rails-react)
        echo "   Languages: Ruby 3.3 + Node.js 20"
        echo "   Database: PostgreSQL 16"
        echo "   Cache: Redis 7"
        echo "   Ports: 3000 (Rails), 3001 (React), 5432 (PostgreSQL)"
        ;;
    python)
        echo "   Languages: Python 3.12"
        echo "   Database: PostgreSQL 16"
        echo "   Cache: Redis 7"
        echo "   Ports: 8000 (App), 5432 (PostgreSQL), 6379 (Redis)"
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if devcontainer already exists
if [ -d "$PROJECT_DIR/.devcontainer" ]; then
    echo "⚠️  Warning: .devcontainer already exists in this project"
    read -p "   Do you want to replace it? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Aborted."
        exit 0
    fi
fi

# Offer to install
read -p "🚀 Install $DETECTED_STACK devcontainer? (Y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "❌ Aborted."
    echo ""
    echo "To install manually:"
    echo "   $SCRIPT_DIR/setup-devcontainer.sh $DETECTED_STACK $PROJECT_DIR"
    exit 0
fi

# Install devcontainer
echo ""
echo "📦 Installing devcontainer..."
"$SCRIPT_DIR/setup-devcontainer.sh" "$DETECTED_STACK" "$PROJECT_DIR"
