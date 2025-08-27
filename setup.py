from setuptools import setup, find_packages

setup(
    name="ghswitch",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        "pywin32",
    ],
    include_package_data=True,
    package_data={
        "ghswitch": ["github_accounts.example.json"],
    },
    entry_points={
        "console_scripts": [
            "ghswitch=ghswitch.cli:main",
        ],
    },
)
