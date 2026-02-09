#!/usr/bin/env python3
"""
Tests for setup_upstream.py

Basic tests to verify the upstream VCS tracking utility works correctly.
"""

import subprocess
import tempfile
import os
import shutil
import sys


def run_command(cmd, cwd=None):
    """Run a command and return output."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def test_help_command():
    """Test that help command works."""
    print("Testing help command...")
    returncode, stdout, stderr = run_command([
        sys.executable,
        "setup_upstream.py",
        "--help"
    ])
    assert returncode == 0, f"Help command failed: {stderr}"
    assert "upstream_url" in stdout, "Help text missing upstream_url"
    print("✓ Help command works")


def test_non_git_directory():
    """Test error handling for non-git directory."""
    print("Testing non-git directory error handling...")
    with tempfile.TemporaryDirectory() as tmpdir:
        returncode, stdout, stderr = run_command([
            sys.executable,
            os.path.abspath("setup_upstream.py"),
            "https://github.com/test/test.git"
        ], cwd=tmpdir)
        assert returncode == 1, "Should fail for non-git directory"
        assert "Not a git repository" in stderr, f"Expected error message not found: {stderr}"
    print("✓ Non-git directory error handling works")


def test_add_upstream():
    """Test adding upstream remote."""
    print("Testing add upstream remote...")
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize git repo
        run_command(["git", "init"], cwd=tmpdir)
        run_command(["git", "config", "user.name", "Test User"], cwd=tmpdir)
        run_command(["git", "config", "user.email", "test@example.com"], cwd=tmpdir)
        
        # Create initial commit
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        run_command(["git", "add", "test.txt"], cwd=tmpdir)
        run_command(["git", "commit", "-m", "Initial commit"], cwd=tmpdir)
        
        # Add upstream
        returncode, stdout, stderr = run_command([
            sys.executable,
            os.path.abspath("setup_upstream.py"),
            "https://github.com/FAIRmat-NFDI/nomad.git"
        ], cwd=tmpdir)
        
        assert returncode == 0, f"Failed to add upstream: {stderr}"
        assert "Successfully added upstream remote" in stdout, f"Success message not found: {stdout}"
        
        # Verify remote was added
        returncode, stdout, _ = run_command(["git", "remote", "-v"], cwd=tmpdir)
        assert "upstream" in stdout, "Upstream remote not found"
        assert "FAIRmat-NFDI/nomad.git" in stdout, "Upstream URL not correct"
    
    print("✓ Add upstream remote works")


def test_duplicate_remote():
    """Test handling of duplicate remote names."""
    print("Testing duplicate remote handling...")
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize git repo
        run_command(["git", "init"], cwd=tmpdir)
        run_command(["git", "config", "user.name", "Test User"], cwd=tmpdir)
        run_command(["git", "config", "user.email", "test@example.com"], cwd=tmpdir)
        
        # Create initial commit
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        run_command(["git", "add", "test.txt"], cwd=tmpdir)
        run_command(["git", "commit", "-m", "Initial commit"], cwd=tmpdir)
        
        # Add upstream manually first
        run_command([
            "git", "remote", "add", "upstream",
            "https://github.com/test/existing.git"
        ], cwd=tmpdir)
        
        # Try to add upstream again with different name to avoid interactive prompt
        returncode, stdout, stderr = run_command([
            sys.executable,
            os.path.abspath("setup_upstream.py"),
            "https://github.com/FAIRmat-NFDI/nomad.git",
            "--remote-name", "upstream2"
        ], cwd=tmpdir)
        
        # Should succeed with different name
        assert returncode == 0, f"Failed with different remote name: {stderr}"
        
        # Verify both remotes exist
        returncode, stdout, _ = run_command(["git", "remote", "-v"], cwd=tmpdir)
        assert "upstream" in stdout, "Original upstream not found"
        assert "upstream2" in stdout, "New upstream2 not found"
    
    print("✓ Duplicate remote handling works")


def main():
    """Run all tests."""
    print("Running tests for setup_upstream.py\n")
    
    try:
        test_help_command()
        test_non_git_directory()
        test_add_upstream()
        test_duplicate_remote()
        
        print("\n✅ All tests passed!")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
