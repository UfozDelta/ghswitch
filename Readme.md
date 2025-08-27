# ghswitch

A Windows CLI tool for quickly switching between multiple GitHub accounts.

## Installation

```bash
pip install -e "path/to/ghswitch"
```

## Setup

1. **Get Personal Access Tokens** for each GitHub account:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate tokens with appropriate scopes

2. **Edit the configuration file** at `%USERPROFILE%\.ghswitch\github_accounts.json`:

```json
[
  {
    "name": "personal",
    "username": "johndoe",
    "email": "john@personal.com",
    "token": "ghp_xxxxxxxxxxxxxxxxxxxx"
  },
  {
    "name": "work",
    "username": "john-work",
    "email": "john@company.com",
    "token": "ghp_yyyyyyyyyyyyyyyyyyyy"
  }
]
```

## Usage

```bash
# List accounts
ghswitch list

# Switch account globally
ghswitch switch --name personal

# Switch account for current repo only
ghswitch switch --name work --local

# Show current account
ghswitch current
```