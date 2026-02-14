#!/usr/bin/env python3
"""Installation script for Sphinx Documentation System."""

import os
import sys
import subprocess

def run_command(cmd):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=True)
    return result.returncode

def main():
    """Main installation function."""
    print("=== Sphinx Documentation System Installation ===")
    
    # Install dependencies
    print("\n1. Installing dependencies...")
    run_command("pip install -r requirements.txt")
    
    # Initialize git (optional)
    print("\n2. Initializing git repository (optional)...")
    if not os.path.exists(".git"):
        try:
            # Check if git is installed
            subprocess.run("git --version", shell=True, check=True, capture_output=True)
            run_command("git init")
            run_command("git add .")
            run_command("git commit -m 'Initial commit'")
        except subprocess.CalledProcessError:
            print("Git is not installed. Skipping git initialization.")
    
    # Create .gitignore file
    print("\n3. Creating .gitignore file...")
    gitignore_content = """# Build output
build/
docs/build/

# Python cache
__pycache__/
*.pyc
*.pyo

# Environment files
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Localization
*.mo
"""
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("\n4. Installation completed successfully!")
    print("\nNext steps:")
    print("- To build the documentation: python scripts/build.py")
    print("- To preview the documentation: python scripts/serve.py")
    print("- To translate the documentation: python scripts/translate.py")

if __name__ == "__main__":
    main()