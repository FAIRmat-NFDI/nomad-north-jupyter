#!/usr/bin/env python3
"""
Setup Upstream VCS Tracking

This script helps configure upstream remote tracking for a local git repository.
It allows users to add an upstream remote and configure branch tracking.
"""

import subprocess
import sys
import argparse
from typing import Optional


def run_command(cmd: list, check: bool = True) -> tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, and stderr."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout.strip() if e.stdout else "", e.stderr.strip() if e.stderr else ""


def check_git_repo() -> bool:
    """Check if current directory is a git repository."""
    returncode, _, _ = run_command(["git", "rev-parse", "--git-dir"], check=False)
    return returncode == 0


def get_current_remotes() -> dict:
    """Get list of current remotes."""
    returncode, stdout, _ = run_command(["git", "remote", "-v"], check=False)
    remotes = {}
    if returncode == 0 and stdout:
        for line in stdout.split('\n'):
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    name, url = parts[0], parts[1]
                    remotes[name] = url
    return remotes


def add_upstream_remote(upstream_url: str, remote_name: str = "upstream") -> bool:
    """Add upstream remote to the repository."""
    print(f"Adding {remote_name} remote: {upstream_url}")
    returncode, stdout, stderr = run_command(
        ["git", "remote", "add", remote_name, upstream_url],
        check=False
    )
    
    if returncode != 0:
        print(f"Error adding remote: {stderr}", file=sys.stderr)
        return False
    
    print(f"Successfully added {remote_name} remote")
    return True


def fetch_upstream(remote_name: str = "upstream") -> bool:
    """Fetch from upstream remote."""
    print(f"Fetching from {remote_name}...")
    returncode, stdout, stderr = run_command(
        ["git", "fetch", remote_name],
        check=False
    )
    
    if returncode != 0:
        print(f"Error fetching from {remote_name}: {stderr}", file=sys.stderr)
        return False
    
    print(f"Successfully fetched from {remote_name}")
    return True


def set_branch_upstream(branch: str, remote_name: str = "upstream", remote_branch: Optional[str] = None) -> bool:
    """Set upstream tracking for a branch."""
    if remote_branch is None:
        remote_branch = branch
    
    tracking_ref = f"{remote_name}/{remote_branch}"
    print(f"Setting upstream tracking for branch '{branch}' to '{tracking_ref}'")
    
    returncode, stdout, stderr = run_command(
        ["git", "branch", f"--set-upstream-to={tracking_ref}", branch],
        check=False
    )
    
    if returncode != 0:
        print(f"Warning: Could not set upstream tracking: {stderr}", file=sys.stderr)
        return False
    
    print(f"Successfully set upstream tracking for '{branch}'")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Setup upstream VCS tracking for a git repository"
    )
    parser.add_argument(
        "upstream_url",
        help="URL of the upstream repository"
    )
    parser.add_argument(
        "--remote-name",
        default="upstream",
        help="Name for the upstream remote (default: upstream)"
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch from upstream after adding"
    )
    parser.add_argument(
        "--set-tracking",
        metavar="BRANCH",
        help="Set upstream tracking for specified branch"
    )
    parser.add_argument(
        "--remote-branch",
        help="Remote branch to track (default: same as local branch)"
    )
    
    args = parser.parse_args()
    
    # Check if we're in a git repository
    if not check_git_repo():
        print("Error: Not a git repository", file=sys.stderr)
        sys.exit(1)
    
    # Check existing remotes
    remotes = get_current_remotes()
    print(f"Current remotes: {list(remotes.keys())}")
    
    if args.remote_name in remotes:
        print(f"Warning: Remote '{args.remote_name}' already exists with URL: {remotes[args.remote_name]}")
        response = input("Do you want to continue? This will not modify the existing remote. (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
    else:
        # Add upstream remote
        if not add_upstream_remote(args.upstream_url, args.remote_name):
            sys.exit(1)
    
    # Fetch if requested
    if args.fetch:
        if not fetch_upstream(args.remote_name):
            sys.exit(1)
    
    # Set branch tracking if requested
    if args.set_tracking:
        if not fetch_upstream(args.remote_name):
            print("Warning: Failed to fetch before setting tracking", file=sys.stderr)
        
        if not set_branch_upstream(args.set_tracking, args.remote_name, args.remote_branch):
            sys.exit(1)
    
    print("\nUpstream VCS tracking setup complete!")
    print(f"\nTo fetch updates from {args.remote_name}:")
    print(f"  git fetch {args.remote_name}")
    print(f"\nTo merge updates from {args.remote_name}:")
    print(f"  git merge {args.remote_name}/main")
    print(f"\nTo see all remotes:")
    print(f"  git remote -v")


if __name__ == "__main__":
    main()
