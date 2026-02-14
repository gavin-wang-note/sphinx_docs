#!/usr/bin/env python3
"""Serve script for Sphinx Documentation System with real-time preview."""

import os
import sys
import subprocess
import argparse
import socket

def find_available_port(start_port=8000, max_attempts=100):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("0.0.0.0", port))
                return port
        except OSError:
            continue
    raise RuntimeError("No available port found")

def run_command(cmd):
    """Run a shell command."""
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def serve_docs(language="en", port=8080):
    """Serve the documentation with real-time preview."""
    # Use sphinx-autobuild for real-time preview
    cmd = f"sphinx-autobuild -b html -d docs/build/doctrees-{language} -D language={language} docs/source docs/build/{language} --host 0.0.0.0 --port {port} --watch src/"
    run_command(cmd)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Serve Sphinx Documentation with Real-time Preview")
    parser.add_argument("--language", "-l", default="en", help="Language to serve (default: en)")
    parser.add_argument("--port", "-p", type=int, default=None, help="Port to use (default: automatically find available port)")
    
    args = parser.parse_args()
    
    # Find available port if none provided
    port = args.port if args.port is not None else find_available_port(start_port=8000)
    
    print("=== Sphinx Documentation Real-time Preview ===")
    print(f"Language: {args.language}")
    print(f"Port: {port}")
    print(f"Preview URL: http://localhost:{port}")
    print("\nPress Ctrl+C to stop the server")
    print("===============================================")
    
    serve_docs(args.language, port)

if __name__ == "__main__":
    main()