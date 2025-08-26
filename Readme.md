# GitHub Credential Switcher (ghswitch)

A Windows tool for quickly switching between multiple GitHub accounts using Git credentials and Windows Credential Manager.

## Setup

1. **Install dependencies:**
   ```bash
   pip install pywin32
   ```

2. **Get Personal Access Tokens:**
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate tokens for each account you want to manage

3. **Create `github_accounts.json`:**
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

**List accounts:**
```bash
python ghswitch.py list
```

**Switch account (global):**
```bash
python ghswitch.py switch --name personal
```

**Switch account (current repo only):**
```bash
python ghswitch.py switch --name work --local
```

**Show current account:**
```bash
python ghswitch.py current
```

## Examples

```bash
# See available accounts
$ python ghswitch.py list
Available accounts:
 - personal (johndoe | john@personal.com)
 - work (john-work | john@company.com)

# Switch to work account
$ python ghswitch.py switch --name work
[:::] Switched to 'work' (john-work / john@company.com)
[:::] Git config updated (global)

# Check current account
$ python ghswitch.py current
[:::] Current active account: john-work (john@company.com)
```

That's it! The tool handles Windows Credential Manager and Git config automatically.