# nomad-north-jupyter

A utility for managing VCS (Version Control System) upstream tracking for NOMAD Jupyter notebook repositories.

## Overview

This repository provides tools to help manage upstream VCS tracking for local repositories. If you have a local repository without upstream tracking configured, you can use the provided script to easily add and configure upstream remotes.

## Features

- Add upstream remote to your local git repository
- Configure branch tracking for synchronization with upstream
- Fetch updates from upstream repository
- Easy-to-use command-line interface

## Usage

### Setting Up Upstream VCS Tracking

If you have a local repository that needs to track an upstream repository:

```bash
python setup_upstream.py <upstream-url> [options]
```

#### Options:

- `upstream-url`: The URL of the upstream repository (required)
- `--remote-name NAME`: Name for the upstream remote (default: "upstream")
- `--fetch`: Fetch from upstream after adding the remote
- `--set-tracking BRANCH`: Set upstream tracking for the specified branch
- `--remote-branch BRANCH`: Remote branch to track (default: same as local branch)

#### Examples:

1. **Add an upstream remote:**
   ```bash
   python setup_upstream.py https://github.com/FAIRmat-NFDI/nomad.git
   ```

2. **Add upstream and fetch immediately:**
   ```bash
   python setup_upstream.py https://github.com/FAIRmat-NFDI/nomad.git --fetch
   ```

3. **Add upstream and set tracking for main branch:**
   ```bash
   python setup_upstream.py https://github.com/FAIRmat-NFDI/nomad.git --fetch --set-tracking main
   ```

4. **Add upstream with custom remote name:**
   ```bash
   python setup_upstream.py https://github.com/FAIRmat-NFDI/nomad.git --remote-name parent --fetch
   ```

### Manual Configuration

You can also manually configure upstream tracking:

```bash
# Add upstream remote
git remote add upstream <upstream-url>

# Fetch from upstream
git fetch upstream

# Set branch to track upstream
git branch --set-upstream-to=upstream/main main
```

### Verifying Configuration

Check your remote configuration:
```bash
git remote -v
```

Check your branch tracking:
```bash
git branch -vv
```

## Configuration File

A sample configuration file `.vcs_config.example` is provided. You can copy and modify it for your needs:

```bash
cp .vcs_config.example .vcs_config
# Edit .vcs_config with your upstream repository details
```

## Common Workflows

### Syncing with Upstream

After setting up upstream tracking:

```bash
# Fetch latest changes from upstream
git fetch upstream

# Merge upstream changes into your current branch
git merge upstream/main

# Or rebase your changes on top of upstream
git rebase upstream/main
```

### Keeping Your Fork Updated

If you have a forked repository:

```bash
# Fetch from upstream
git fetch upstream

# Checkout your main branch
git checkout main

# Merge upstream changes
git merge upstream/main

# Push to your fork
git push origin main
```

## Requirements

- Python 3.9 or higher
- Git installed and configured

## License

This project is part of the FAIRmat-NFDI NOMAD ecosystem.