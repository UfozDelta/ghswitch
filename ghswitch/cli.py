import json
import argparse
import subprocess
import sys
import win32cred
import importlib.resources as pkg_resources
import os

CRED_TYPE = win32cred.CRED_TYPE_GENERIC
TARGET_NAME = "git:https://github.com"  # Git for Windows uses this target

def load_accounts(filepath=None):
    if filepath and os.path.exists(filepath):
        # user-supplied file still works
        with open(filepath, "r") as f:
            return json.load(f)
    else:
        # fallback: use packaged example JSON
        with pkg_resources.open_text("ghswitch", "github_accounts.example.json") as f:
            return json.load(f)


def switch_account(name, accounts, global_config=True):
    account = next((acc for acc in accounts if acc["name"] == name), None)
    if not account:
        print(f"[!] Account '{name}' not found.")
        return

    # Store PAT in Windows Credential Manager
    cred = {
    'Type': CRED_TYPE,
    'TargetName': TARGET_NAME,
    'UserName': account['username'],
    'CredentialBlob': account['token'],  # keep as str
    'Persist': win32cred.CRED_PERSIST_LOCAL_MACHINE
    }
    win32cred.CredWrite(cred, 0)

    # Update Git config
    scope = "--global" if global_config else ""
    subprocess.run(["git", "config", scope, "user.name", account['username']], check=True)
    subprocess.run(["git", "config", scope, "user.email", account['email']], check=True)

    print(f"[:::] Switched to '{name}' ({account['username']} / {account['email']})")
    print(f"[:::] Git config updated ({'global' if global_config else 'local'})")


def list_accounts(accounts):
    print("Available accounts:")
    for acc in accounts:
        print(f" - {acc['name']} ({acc['username']} | {acc['email']})")


def current_account():
    try:
        cred = win32cred.CredRead(TARGET_NAME, CRED_TYPE)
        username = cred["UserName"]

        # Try to get email from Git config
        email = subprocess.run(
            ["git", "config", "--get", "user.email"],
            capture_output=True, text=True
        ).stdout.strip()

        print(f"[:::] Current active account: {username} ({email})")
    except Exception:
        print("[!] No active GitHub credentials found in Windows Credential Manager.")

def show_help():
    print("""
GitHub Credential Switcher (ghswitch)
-------------------------------------

Commands:
  list               Show all available accounts from the JSON file
  switch --name NAME Switch to a given account (updates Credential Manager + Git config)
    --local          Apply Git config only to the current repository (instead of global)
  current            Show the currently active account (from Credential Manager + Git config)
  help               Show this help message

Examples:
  ghswitch list
  ghswitch switch --name work
  ghswitch switch --name personal --local
  ghswitch current
""")

def main():
    parser = argparse.ArgumentParser(description="GitHub Credential Switcher (Windows)", add_help=False)
    parser.add_argument("action", choices=["list", "switch", "current", "help"], help="Action to perform")
    parser.add_argument("--name", help="Account name (for switch)")
    parser.add_argument("--file", default="github_accounts.json", help="Accounts file")
    parser.add_argument("--local", action="store_true", help="Apply Git config locally instead of globally")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
    args = parser.parse_args()

    if args.help or args.action == "help":
        show_help()
        sys.exit(0)

    if args.action == "list":
        accounts = load_accounts(args.file)
        list_accounts(accounts)
    elif args.action == "switch":
        if not args.name:
            print("[!] You must provide --name for switch")
        else:
            accounts = load_accounts(args.file)
            switch_account(args.name, accounts, global_config=not args.local)
    elif args.action == "current":
        current_account()

# This makes "python ghswitch.py" still work
if __name__ == "__main__":
    main()