#!/usr/bin/env python3
"""
Intelligent DevContainer Builder
Analyzes project structure and automatically generates appropriate devcontainer configuration
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional

SCRIPT_DIR = Path(__file__).parent.absolute()

class ProjectAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).absolute()
        self.findings = []
        self.scores = {}
        
    def analyze(self) -> Tuple[Optional[str], float, List[str]]:
        """Analyze project and return (stack, confidence, findings)"""
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {self.project_path}")
            
        self._check_rails()
        self._check_strapi()
        self._check_go_react()
        self._check_python()
        self._check_nodejs()
        
        if not self.scores:
            return None, 0.0, ["No recognizable project structure found"]
            
        # Get stack with highest score
        stack = max(self.scores.items(), key=lambda x: x[1])
        return stack[0], stack[1], self.findings
    
    def _check_rails(self):
        """Check for Rails project"""
        gemfile = self.project_path / "Gemfile"
        if gemfile.exists():
            content = gemfile.read_text()
            if "rails" in content.lower():
                score = 90
                self.findings.append("✓ Found Gemfile with Rails")
                
                # Check for React frontend
                if (self.project_path / "frontend" / "package.json").exists():
                    self.scores["rails-react"] = 95
                    self.findings.append("✓ Found frontend/package.json (React)")
                elif any((self.project_path / "app" / "javascript").glob("*.jsx")) or \
                     any((self.project_path / "app" / "javascript").glob("*.tsx")):
                    self.scores["rails-react"] = 85
                    self.findings.append("✓ Found React components in app/javascript")
                else:
                    self.scores["rails"] = score
                    
    def _check_strapi(self):
        """Check for Strapi project"""
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                
                if any("strapi" in dep for dep in deps.keys()):
                    self.scores["strapi"] = 95
                    self.findings.append("✓ Found Strapi in package.json dependencies")
                    
                    # Check for Strapi directories
                    if (self.project_path / "src" / "api").exists():
                        self.scores["strapi"] += 5
                        self.findings.append("✓ Found Strapi API structure")
                        
            except json.JSONDecodeError:
                pass
                
    def _check_go_react(self):
        """Check for Go + React project"""
        go_mod = self.project_path / "go.mod"
        backend_go_mod = self.project_path / "backend" / "go.mod"
        frontend_pkg = self.project_path / "frontend" / "package.json"
        
        has_go = go_mod.exists() or backend_go_mod.exists()
        has_react = frontend_pkg.exists()
        
        if has_go and has_react:
            self.scores["go-react"] = 95
            self.findings.append("✓ Found Go backend (go.mod)")
            self.findings.append("✓ Found React frontend (package.json)")
            
            # Check for common Go web frameworks
            if backend_go_mod.exists():
                content = backend_go_mod.read_text()
                if any(fw in content for fw in ["gin", "echo", "fiber", "chi"]):
                    self.findings.append("✓ Found Go web framework")
                    
        elif has_go:
            # Might be Go-only project but suggest go-react template
            backend_dir = self.project_path / "backend"
            cmd_dir = self.project_path / "cmd"
            
            if backend_dir.exists() or cmd_dir.exists():
                self.scores["go-react"] = 60
                self.findings.append("✓ Found Go project structure")
                self.findings.append("? Could be extended with React frontend")
                
    def _check_python(self):
        """Check for Python project"""
        requirements = self.project_path / "requirements.txt"
        pyproject = self.project_path / "pyproject.toml"
        setup_py = self.project_path / "setup.py"
        
        has_python = requirements.exists() or pyproject.exists() or setup_py.exists()
        
        if has_python:
            score = 70
            self.findings.append("✓ Found Python project files")
            
            # Check for web frameworks
            if requirements.exists():
                content = requirements.read_text().lower()
                if "fastapi" in content:
                    score = 95
                    self.findings.append("✓ Found FastAPI framework")
                elif "django" in content:
                    score = 95
                    self.findings.append("✓ Found Django framework")
                elif "flask" in content:
                    score = 95
                    self.findings.append("✓ Found Flask framework")
                elif "uvicorn" in content or "gunicorn" in content:
                    score = 85
                    self.findings.append("✓ Found ASGI/WSGI server")
                    
            if pyproject.exists():
                content = pyproject.read_text().lower()
                if any(fw in content for fw in ["fastapi", "django", "flask"]):
                    score = max(score, 95)
                    self.findings.append("✓ Found web framework in pyproject.toml")
                    
            self.scores["python"] = score
            
    def _check_nodejs(self):
        """Check for generic Node.js project"""
        package_json = self.project_path / "package.json"
        
        if package_json.exists() and "strapi" not in self.scores:
            try:
                data = json.loads(package_json.read_text())
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                
                # Check for React/Next.js
                if "react" in deps or "next" in deps:
                    self.scores["go-react"] = 50
                    self.findings.append("? Found React project (could add Go backend)")
                # Check for Express/Fastify
                elif "express" in deps or "fastify" in deps or "koa" in deps:
                    self.scores["strapi"] = 60
                    self.findings.append("? Found Node.js web framework")
                    
            except json.JSONDecodeError:
                pass

def print_stack_info(stack: str):
    """Print information about the stack"""
    stacks = {
        "rails": {
            "name": "Ruby on Rails",
            "languages": "Ruby 3.3 + Rails",
            "database": "PostgreSQL 16",
            "cache": "Redis 7",
            "ports": "3000 (Rails), 5432 (PostgreSQL)"
        },
        "strapi": {
            "name": "Strapi CMS",
            "languages": "Node.js 20",
            "database": "PostgreSQL 16",
            "cache": "-",
            "ports": "1337 (Strapi), 5432 (PostgreSQL)"
        },
        "go-react": {
            "name": "Go + React",
            "languages": "Go 1.22 + Node.js 20",
            "database": "PostgreSQL 16",
            "cache": "Redis 7",
            "ports": "8080 (Go API), 3000 (React), 5432 (PostgreSQL)"
        },
        "rails-react": {
            "name": "Rails + React",
            "languages": "Ruby 3.3 + Node.js 20",
            "database": "PostgreSQL 16",
            "cache": "Redis 7",
            "ports": "3000 (Rails), 3001 (React), 5432 (PostgreSQL)"
        },
        "python": {
            "name": "Python",
            "languages": "Python 3.12",
            "database": "PostgreSQL 16",
            "cache": "Redis 7",
            "ports": "8000 (App), 5432 (PostgreSQL), 6379 (Redis)"
        }
    }
    
    if stack in stacks:
        info = stacks[stack]
        print(f"\n📋 Stack: {info['name']}")
        print(f"   Languages: {info['languages']}")
        print(f"   Database: {info['database']}")
        print(f"   Cache: {info['cache']}")
        print(f"   Ports: {info['ports']}")

def install_devcontainer(stack: str, project_path: Path, auto_open: bool = False):
    """Install devcontainer and optionally open in VS Code"""
    setup_script = SCRIPT_DIR / "setup-devcontainer.sh"
    
    if not setup_script.exists():
        print(f"❌ Setup script not found: {setup_script}")
        return False
        
    print(f"\n📦 Installing {stack} devcontainer...")
    
    try:
        subprocess.run(
            [str(setup_script), stack, str(project_path)],
            check=True
        )
        
        if auto_open:
            print("\n🚀 Opening project in VS Code...")
            subprocess.run(["code", str(project_path)], check=False)
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Intelligent DevContainer Builder - Auto-detect and setup devcontainers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/project               # Analyze and prompt for installation
  %(prog)s /path/to/project --auto        # Analyze and auto-install
  %(prog)s /path/to/project --stack rails # Force specific stack
  %(prog)s /path/to/project --open        # Install and open in VS Code
        """
    )
    
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to project directory (default: current directory)"
    )
    
    parser.add_argument(
        "-s", "--stack",
        choices=["rails", "strapi", "go-react", "rails-react", "python"],
        help="Force specific stack (skip detection)"
    )
    
    parser.add_argument(
        "-a", "--auto",
        action="store_true",
        help="Auto-install without prompting"
    )
    
    parser.add_argument(
        "-o", "--open",
        action="store_true",
        help="Open project in VS Code after installation"
    )
    
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List available stacks"
    )
    
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Analyze only, don't install"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("Available DevContainer Stacks:\n")
        for stack in ["rails", "strapi", "go-react", "rails-react", "python"]:
            print_stack_info(stack)
        return 0
    
    project_path = Path(args.project_path).absolute()
    
    print(f"🔍 Analyzing project: {project_path}\n")
    print("━" * 60)
    
    # Force stack or detect
    if args.stack:
        stack = args.stack
        confidence = 100.0
        findings = [f"✓ Stack forced to: {stack}"]
    else:
        analyzer = ProjectAnalyzer(str(project_path))
        stack, confidence, findings = analyzer.analyze()
    
    # Display findings
    print("\n📊 Detection Results:")
    for finding in findings:
        print(f"   {finding}")
    
    if not stack:
        print("\n❌ Could not detect project type!")
        print("\n💡 Use --stack to specify manually:")
        print("   python devcontainer-builder.py /path/to/project --stack rails")
        return 1
    
    # Display confidence
    if confidence >= 90:
        emoji = "✅"
        level = "HIGH"
    elif confidence >= 70:
        emoji = "⚠️"
        level = "MEDIUM"
    else:
        emoji = "❓"
        level = "LOW"
    
    print(f"\n{emoji} Recommended: {stack} (confidence: {level} - {confidence:.0f}%)")
    print_stack_info(stack)
    print("\n" + "━" * 60)
    
    # Check if devcontainer exists
    devcontainer_path = project_path / ".devcontainer"
    if devcontainer_path.exists() and not args.auto:
        print(f"\n⚠️  Warning: .devcontainer already exists")
        response = input("   Replace it? (y/N): ").strip().lower()
        if response not in ["y", "yes"]:
            print("❌ Aborted.")
            return 0
    
    # Dry run mode
    if args.dry_run:
        print("\n🔍 Dry run mode - no changes made")
        print(f"\nTo install: {SCRIPT_DIR}/setup-devcontainer.sh {stack} {project_path}")
        return 0
    
    # Prompt or auto-install
    if not args.auto:
        response = input(f"\n🚀 Install {stack} devcontainer? (Y/n): ").strip().lower()
        if response in ["n", "no"]:
            print("❌ Aborted.")
            print(f"\nTo install manually: {SCRIPT_DIR}/setup-devcontainer.sh {stack} {project_path}")
            return 0
    
    # Install
    success = install_devcontainer(stack, project_path, args.open)
    
    if success:
        print("\n✅ DevContainer installed successfully!")
        if not args.open:
            print("\n💡 Next steps:")
            print(f"   1. cd {project_path}")
            print(f"   2. code .")
            print(f"   3. Cmd+Shift+P → 'Dev Containers: Reopen in Container'")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
