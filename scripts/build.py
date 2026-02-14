#!/usr/bin/env python3
"""Build script for Sphinx Documentation System."""

import os
import sys
import subprocess
import argparse

def run_command(cmd):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=True)
    return result.returncode

def build_docs(language="en", builder="html"):
    """Build the documentation."""
    # Create build directory if it doesn't exist
    if not os.path.exists("docs/build"):
        os.makedirs("docs/build")
    
    # Build the documentation
    cmd = f"sphinx-build -b {builder} -D language={language} docs/source docs/build/{language}"
    run_command(cmd)
    
    # For PDF builder, copy PDF to root build directory
    if builder == 'pdf':
        pdf_file = os.path.join("docs/build", language, "SphinxDocumentation.pdf")
        if os.path.exists(pdf_file):
            # Create html build directory if it doesn't exist
            html_dir = os.path.join("docs/build", language, "html")
            if os.path.exists(html_dir):
                import shutil
                shutil.copy(pdf_file, html_dir)
                print(f"PDF file copied to {html_dir}/")
    
    # For HTML builder, check if PDF exists and copy it
    if builder in ['html', 'dirhtml']:
        pdf_file = os.path.join("docs/build", language, "pdf", "SphinxDocumentation.pdf")
        if os.path.exists(pdf_file):
            import shutil
            shutil.copy(pdf_file, os.path.join("docs/build", language))
            print(f"PDF file copied to docs/build/{language}/")
    
    print(f"\nDocumentation built successfully in docs/build/{language}/")

def build_all_languages(builder="html"):
    """Build documentation for all languages."""
    languages = ["en", "zh"]
    for lang in languages:
        build_docs(lang, builder)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Build Sphinx Documentation")
    parser.add_argument("--language", "-l", default="en", help="Language to build (default: en)")
    parser.add_argument("--builder", "-b", default="html", help="Builder to use (default: html)")
    parser.add_argument("--all", "-a", action="store_true", help="Build all languages")
    
    args = parser.parse_args()
    
    print("=== Sphinx Documentation Build ===")
    
    if args.all:
        build_all_languages(args.builder)
    else:
        build_docs(args.language, args.builder)
    
    print("\nBuild completed successfully!")

if __name__ == "__main__":
    main()