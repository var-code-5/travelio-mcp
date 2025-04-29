#!/usr/bin/env python
import argparse
import subprocess
import os
import sys

def run_command(cmd):
    """Run a command and print its output."""
    process = subprocess.Popen("uv run "+cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    return process.poll()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Alembic migration helper")
    parser.add_argument("command", choices=["init", "migrate", "upgrade", "downgrade", "history", "current"],
                      help="Migration command to run")
    parser.add_argument("--message", "-m", help="Migration message (for 'migrate' command)")
    parser.add_argument("--revision", "-r", help="Revision identifier (for 'upgrade/downgrade' commands)")
    
    args = parser.parse_args()
    
    if args.command == "init":
        cmd = "alembic revision --autogenerate -m 'Initial migration'"
        run_command(cmd)
    
    elif args.command == "migrate":
        message = args.message or "Update schema"
        cmd = f"alembic revision --autogenerate -m '{message}'"
        run_command(cmd)
    
    elif args.command == "upgrade":
        revision = args.revision or "head"
        cmd = f"alembic upgrade {revision}"
        run_command(cmd)
    
    elif args.command == "downgrade":
        revision = args.revision or "-1"
        cmd = f"alembic downgrade {revision}"
        run_command(cmd)
    
    elif args.command == "history":
        cmd = "alembic history"
        run_command(cmd)
    
    elif args.command == "current":
        cmd = "alembic current"
        run_command(cmd)
