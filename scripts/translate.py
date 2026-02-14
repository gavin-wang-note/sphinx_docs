#!/usr/bin/env python3
"""Translation script for Sphinx Documentation System."""

import os
import sys
import subprocess
import argparse

def run_command(cmd):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=True)
    return result.returncode

def extract_messages():
    """Extract messages for translation."""
    # Create _locale directory if it doesn't exist
    if not os.path.exists("docs/_locale"):
        os.makedirs("docs/_locale")
    
    # Extract messages
    cmd = "sphinx-build -b gettext docs/source docs/_locale/gettext"
    run_command(cmd)
    
    print("\nMessages extracted successfully to docs/_locale/gettext/")

def update_translations(language):
    """Update translations for a specific language."""
    # Create language directory if it doesn't exist
    lang_dir = f"docs/_locale/{language}/LC_MESSAGES"
    if not os.path.exists(lang_dir):
        os.makedirs(lang_dir)
    
    # Update pot files
    extract_messages()
    
    # Update po files
    cmd = f"sphinx-intl update -p docs/_locale/gettext -l {language} --locale-dir docs/_locale"
    run_command(cmd)
    
    print(f"\nTranslations updated for {language} in docs/_locale/{language}/LC_MESSAGES/")

def compile_translations():
    """Compile all translations."""
    cmd = "sphinx-intl build --locale-dir docs/_locale"
    run_command(cmd)
    
    print("\nTranslations compiled successfully!")

def init_translation(language):
    """Initialize translation for a new language."""
    # Extract messages first
    extract_messages()
    
    # Initialize translation
    cmd = f"sphinx-intl update -p docs/_locale/gettext -l {language} --locale-dir docs/_locale"
    run_command(cmd)
    
    print(f"\nTranslation initialized for {language}!")
    print(f"Now you can edit the .po files in docs/_locale/{language}/LC_MESSAGES/")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Sphinx Documentation Translation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract messages for translation")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update translations for a specific language")
    update_parser.add_argument("language", help="Language code (e.g., zh, fr, de)")
    
    # Compile command
    compile_parser = subparsers.add_parser("compile", help="Compile all translations")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize translation for a new language")
    init_parser.add_argument("language", help="Language code (e.g., zh, fr, de)")
    
    args = parser.parse_args()
    
    print("=== Sphinx Documentation Translation Tool ===")
    
    if args.command == "extract":
        extract_messages()
    elif args.command == "update":
        update_translations(args.language)
    elif args.command == "compile":
        compile_translations()
    elif args.command == "init":
        init_translation(args.language)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()