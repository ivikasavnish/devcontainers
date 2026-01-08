# DevContainer Builder & Auto-Detection Guide

Intelligent tools to automatically detect your project type and setup the appropriate devcontainer.

## 🚀 Quick Start

### Method 1: Unified CLI (Recommended)
```bash
# Auto-detect and setup
~/devcontainers/devcontainer-cli auto /path/to/project

# Force specific stack
~/devcontainers/devcontainer-cli install rails /path/to/project

# Detect only (no changes)
~/devcontainers/devcontainer-cli detect /path/to/project

# List all stacks
~/devcontainers/devcontainer-cli list

# Open in VS Code
~/devcontainers/devcontainer-cli open /path/to/project
```

### Method 2: Bash Auto-Detect
```bash
~/devcontainers/auto-detect.sh /path/to/project
```

### Method 3: Python Builder (Advanced)
```bash
# Interactive mode
python3 ~/devcontainers/devcontainer-builder.py /path/to/project

# Auto-install
python3 ~/devcontainers/devcontainer-builder.py /path/to/project --auto

# Dry run (detect only)
python3 ~/devcontainers/devcontainer-builder.py /path/to/project --dry-run

# Force stack
python3 ~/devcontainers/devcontainer-builder.py /path/to/project --stack rails

# Install and open in VS Code
python3 ~/devcontainers/devcontainer-builder.py /path/to/project --auto --open
```

## 📋 Tools Overview

### 1. **devcontainer-cli** - Unified Interface
Single command-line tool for all operations.

**Commands:**
- `auto` - Auto-detect and setup
- `build` - Use Python builder
- `install` - Install specific stack  
- `list` - Show available stacks
- `detect` - Detect project type only
- `open` - Open in VS Code
- `remove` - Remove devcontainer

**Examples:**
```bash
devcontainer-cli auto .                    # Current directory
devcontainer-cli install python ~/myapp    # Force Python stack
devcontainer-cli detect ~/existing-project # Detect only
devcontainer-cli list                      # Show all stacks
```

### 2. **auto-detect.sh** - Bash Detection
Lightweight bash script for quick detection and setup.

**Features:**
- Fast file-based detection
- Interactive prompts
- No dependencies
- Perfect for quick analysis

**Usage:**
```bash
./auto-detect.sh /path/to/project
```

### 3. **devcontainer-builder.py** - Python Builder
Advanced Python tool with detailed analysis and options.

**Features:**
- Intelligent confidence scoring
- Detailed project analysis
- Multiple detection strategies
- Command-line options for automation

**Usage:**
```bash
# Basic
python3 devcontainer-builder.py /path/to/project

# Advanced options
python3 devcontainer-builder.py /path/to/project \
    --auto \           # No prompts
    --open \           # Open in VS Code
    --stack python \   # Force stack
    --dry-run          # Detect only
```

## 🔍 Detection Logic

### Rails Projects
**Detected by:**
- ✅ `Gemfile` with "rails" dependency
- ✅ Standard Rails directory structure
- ✅ Optional: `frontend/` for Rails + React

**Confidence:** HIGH (90-95%)

### Strapi Projects
**Detected by:**
- ✅ `package.json` with "@strapi/*" dependencies
- ✅ `src/api/` directory structure
- ✅ Strapi configuration files

**Confidence:** HIGH (95-100%)

### Go + React Projects
**Detected by:**
- ✅ `go.mod` or `backend/go.mod`
- ✅ `frontend/package.json`
- ✅ Separate backend/frontend directories
- ✅ Go web frameworks (Gin, Echo, Fiber)

**Confidence:** HIGH (95%) or MEDIUM (60% for Go-only)

### Rails + React Projects
**Detected by:**
- ✅ `Gemfile` with Rails
- ✅ `frontend/package.json` or React in `app/javascript`
- ✅ JSX/TSX files

**Confidence:** HIGH (85-95%)

### Python Projects
**Detected by:**
- ✅ `requirements.txt` or `pyproject.toml`
- ✅ Web frameworks: FastAPI, Django, Flask
- ✅ ASGI/WSGI servers: Uvicorn, Gunicorn

**Confidence:** HIGH (95%) for web frameworks, MEDIUM (70%) for general Python

## 📊 Confidence Levels

| Score | Level | Action |
|-------|-------|--------|
| 90-100% | ✅ HIGH | Auto-recommend with confidence |
| 70-89% | ⚠️ MEDIUM | Suggest with caution |
| 50-69% | ❓ LOW | Prompt user for confirmation |
| <50% | ❌ UNKNOWN | Manual selection required |

## 🛠️ Advanced Usage

### Batch Processing
```bash
#!/bin/bash
# Setup devcontainers for multiple projects

for project in ~/projects/*/; do
    echo "Processing: $project"
    ~/devcontainers/devcontainer-cli auto "$project"
done
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Setup DevContainer
  run: |
    ~/devcontainers/devcontainer-builder.py . \
      --auto \
      --dry-run || exit 0
```

### Custom Detection
```python
# Extend devcontainer-builder.py
class CustomAnalyzer(ProjectAnalyzer):
    def _check_custom_stack(self):
        # Your custom detection logic
        if (self.project_path / "special.config").exists():
            self.scores["custom-stack"] = 95
            self.findings.append("✓ Found custom stack")
```

## 🎯 Use Cases

### 1. New Project Setup
```bash
# Create Rails project
rails new myapp
cd myapp

# Auto-setup devcontainer
devcontainer-cli auto .

# Open in VS Code
code .
```

### 2. Existing Project Migration
```bash
# Clone repository
git clone https://github.com/user/project
cd project

# Detect and setup
devcontainer-cli auto .

# Start development
code .
# Then: Cmd+Shift+P → "Dev Containers: Reopen in Container"
```

### 3. Multi-Stack Monorepo
```bash
# Setup different stacks for different services
devcontainer-cli install go-react ./backend
devcontainer-cli install python ./ml-service
devcontainer-cli install rails ./admin-panel
```

### 4. Team Onboarding
```bash
# New team member setup (single command!)
devcontainer-cli auto ~/workspace/company-project
```

## 🔧 Customization

### Add Global Alias
```bash
# Add to ~/.zshrc or ~/.bashrc
alias dc='~/devcontainers/devcontainer-cli'

# Now use:
dc auto .
dc list
dc install python /path/to/project
```

### Create Symlink
```bash
# Add to PATH
sudo ln -s ~/devcontainers/devcontainer-cli /usr/local/bin/devcontainer

# Now use from anywhere:
devcontainer auto .
```

### Environment Variables
```bash
# Configure default behavior
export DEVCONTAINER_AUTO_OPEN=1      # Auto-open VS Code
export DEVCONTAINER_NO_PROMPT=1      # Skip confirmations
export DEVCONTAINER_DEFAULT_STACK=python  # Default stack
```

## 📝 Project Structure Detection Examples

### Example 1: Rails API + React
```
myproject/
├── Gemfile              ✅ Rails detected
├── app/
├── config/
└── frontend/
    └── package.json     ✅ React detected
    
→ Result: rails-react (95% confidence)
```

### Example 2: FastAPI Python
```
myproject/
├── requirements.txt     ✅ Python detected
│   └── fastapi==0.109.0 ✅ FastAPI detected
├── main.py
└── app/
    
→ Result: python (95% confidence)
```

### Example 3: Go Microservice
```
myproject/
├── go.mod               ✅ Go detected
├── backend/
│   ├── main.go
│   └── internal/
└── frontend/
    └── package.json     ✅ React detected
    
→ Result: go-react (95% confidence)
```

### Example 4: Strapi CMS
```
myproject/
├── package.json
│   └── @strapi/strapi   ✅ Strapi detected
├── src/
│   └── api/             ✅ Strapi structure detected
└── config/
    
→ Result: strapi (100% confidence)
```

## 🐛 Troubleshooting

### Detection Not Working
```bash
# Enable debug output
DEVCONTAINER_DEBUG=1 devcontainer-cli detect /path/to/project

# Use Python builder for detailed analysis
python3 ~/devcontainers/devcontainer-builder.py /path/to/project --dry-run

# Force specific stack
devcontainer-cli install <stack> /path/to/project
```

### Wrong Stack Detected
```bash
# Override with correct stack
devcontainer-cli install python /path/to/project

# Or use Python builder
python3 ~/devcontainers/devcontainer-builder.py /path/to/project --stack python
```

### Multiple Matches
If project has mixed technologies:
1. Review detection output
2. Choose most relevant stack
3. Use `--stack` to force selection

## 📚 Related Documentation

- Main README: `~/devcontainers/README.md`
- Quick Reference: `~/devcontainers/QUICK-REFERENCE.md`
- Stack-specific docs: `~/devcontainers/<stack>/README.md`

## 🎓 Tips & Best Practices

1. **Always review detection results** before installing
2. **Use dry-run mode** (`--dry-run`) for exploration
3. **Commit `.devcontainer`** to version control
4. **Document custom stacks** in project README
5. **Test devcontainer** after installation
6. **Share with team** for consistent environments

## 🚀 Next Steps

After setting up devcontainer:
1. Open project in VS Code: `code /path/to/project`
2. Reopen in container: `Cmd+Shift+P` → "Dev Containers: Reopen in Container"
3. Wait for setup to complete
4. Start coding!

## 📄 License

MIT - Use freely in your projects!
