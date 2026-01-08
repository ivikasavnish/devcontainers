# DevContainer Templates & CLI

A collection of production-ready DevContainer templates and an intelligent CLI for automating development environment setup.

## 🚀 Quick Start

```bash
# Install CLI
curl -fsSL https://raw.githubusercontent.com/ivikasavnish/devcontainers/main/devcontainer-cli -o /usr/local/bin/devcontainer
chmod +x /usr/local/bin/devcontainer

# Auto-detect and setup your project
devcontainer auto /path/to/your/project

# Or install a specific stack
devcontainer install rails /path/to/your/project
```

## 📦 Available Stacks

### 1. Rails
**Path:** `rails/.devcontainer/`  
**Stack:** Ruby 3.3 + Rails + PostgreSQL + Redis  
**Ports:** 3000 (Rails), 5432 (PostgreSQL)  
**Use for:** Full-stack Rails applications

### 2. Strapi
**Path:** `strapi/.devcontainer/`  
**Stack:** Node.js 20 + Strapi CMS + PostgreSQL  
**Ports:** 1337 (Strapi), 5432 (PostgreSQL)  
**Use for:** Headless CMS projects

### 3. Go + React
**Path:** `go-react/.devcontainer/`  
**Stack:** Go 1.22 + Node.js 20 + PostgreSQL + Redis  
**Ports:** 8080 (Go API), 3000 (React), 5432 (PostgreSQL)  
**Use for:** Go backend with React frontend

### 4. Rails + React
**Path:** `rails-react/.devcontainer/`  
**Stack:** Ruby 3.3 + Rails API + Node.js 20 + React + PostgreSQL + Redis  
**Ports:** 3000 (Rails), 3001 (React), 5432 (PostgreSQL)  
**Use for:** Rails API with React frontend

### 5. Python
**Path:** `python/.devcontainer/`  
**Stack:** Python 3.12 + PostgreSQL + Redis  
**Ports:** 8000 (App), 5432 (PostgreSQL), 6379 (Redis)  
**Use for:** FastAPI, Django, Flask applications

## 🚀 Setup Methods

### Method 1: Auto-Detect (Recommended!)
```bash
# Unified CLI - detects project type automatically
~/devcontainers/devcontainer-cli auto /path/to/project

# Or use Python builder with advanced options
python3 ~/devcontainers/devcontainer-builder.py /path/to/project --auto --open

# Or bash auto-detect
~/devcontainers/auto-detect.sh /path/to/project
```

### Method 2: Manual Stack Selection
```bash
# Copy specific stack
cp -r ~/devcontainers/rails/.devcontainer /path/to/your/project/

# Or use setup script
~/devcontainers/setup-devcontainer.sh rails /path/to/your/project

# Or use CLI
~/devcontainers/devcontainer-cli install rails /path/to/your/project
```

### Method 3: VS Code Manual
1. Copy `.devcontainer` folder to project root
2. Open in VS Code: `code /path/to/your/project`
3. `Cmd+Shift+P` → "Dev Containers: Reopen in Container"
4. Wait for setup - dependencies install automatically!

## Features

All containers include:
- ✅ Production-ready tech stacks
- ✅ Pre-configured databases (PostgreSQL)
- ✅ Caching layers (Redis where applicable)
- ✅ Language-specific VS Code extensions
- ✅ Auto-install dependencies
- ✅ Oh-My-Zsh terminal
- ✅ Git & GitHub CLI
- ✅ Port forwarding configured

## Project Structure Requirements

### Go + React
```
project/
├── .devcontainer/
├── backend/      # Go code (main.go, go.mod)
└── frontend/     # React app (package.json)
```

### Rails + React
```
project/
├── .devcontainer/
├── app/          # Rails app
├── config/
├── frontend/     # React app (package.json)
└── Gemfile
```

### Others
Place `.devcontainer/` at project root with standard framework structure.

## Customization

Each devcontainer is fully customizable:
- **Extensions:** Edit `devcontainer.json` → `customizations.vscode.extensions`
- **Ports:** Modify `forwardPorts` array
- **Environment:** Update `docker-compose.yml` → `environment`
- **Commands:** Change `postCreateCommand` for different setup steps

## Troubleshooting

**Container won't start:**
- Ensure Docker is running
- Check Docker has enough resources (4GB+ RAM recommended)

**Port already in use:**
- Change port in `docker-compose.yml` and `devcontainer.json`

**Dependencies fail to install:**
- Check your `requirements.txt`, `package.json`, `Gemfile`, or `go.mod` for errors
- Rebuild container: `Cmd+Shift+P` → "Dev Containers: Rebuild Container"

## 🤖 Auto-Detection Features

The builder tools intelligently detect your project type:

- **Rails**: Detects `Gemfile` with rails dependency
- **Strapi**: Finds `package.json` with @strapi packages
- **Go + React**: Identifies `go.mod` + `frontend/package.json`
- **Rails + React**: Rails project with React frontend
- **Python**: Detects FastAPI, Django, Flask in requirements

**Learn more:** [BUILDER-GUIDE.md](BUILDER-GUIDE.md)

## 📚 Available Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `devcontainer-cli` | Unified CLI interface | All-in-one tool (recommended) |
| `auto-detect.sh` | Bash auto-detection | Quick analysis, no dependencies |
| `devcontainer-builder.py` | Python builder | Advanced options, detailed analysis |
| `setup-devcontainer.sh` | Manual installer | Force specific stack |

## 🎓 Examples

```bash
# Detect project type only (no installation)
devcontainer-cli detect /path/to/project

# List all available stacks
devcontainer-cli list

# Install and open in VS Code
python3 devcontainer-builder.py /path/to/project --auto --open

# Force specific stack
devcontainer-cli install python /path/to/project

# Remove devcontainer
devcontainer-cli remove /path/to/project
```

## Requirements

- VS Code with "Dev Containers" extension
- Docker Desktop (running)
- 4GB+ RAM recommended
- 10GB+ free disk space
- Optional: Python 3.8+ for advanced builder

## 📖 Documentation

- **[BUILDER-GUIDE.md](BUILDER-GUIDE.md)** - Auto-detection and builder tools
- **[QUICK-REFERENCE.md](QUICK-REFERENCE.md)** - Command cheat sheet
- **Stack READMEs** - Individual stack documentation

## 💡 Pro Tips

```bash
# Add CLI to PATH
alias dc='~/devcontainers/devcontainer-cli'

# Now use anywhere
dc auto .
dc list
dc install python ~/myproject
```

## License

MIT - Use freely in your projects!
