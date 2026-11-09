"""Create a GitHub repository with a starter README from the command line.

Uses the GitHub API through PyGithub. The access token is read from the
GITHUB_TOKEN environment variable so it never ends up in the source code.

Example:
    export GITHUB_TOKEN=ghp_xxx
    python github_bot.py my-new-repo -d "Experiments with FastAPI" --private --gitignore Python
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any


def build_readme(name: str, description: str) -> str:
    """Return the Markdown for the repository's first README."""
    lines = [f"# {name}", ""]
    if description:
        lines += [description, ""]
    lines += ["## Getting started", "", "_Coming soon._", ""]
    return "\n".join(lines)


def create_repository(
    client: Any,
    name: str,
    description: str = "",
    private: bool = False,
    gitignore: str | None = None,
    license_template: str | None = None,
) -> Any:
    """Create ``name`` on the authenticated account and commit a README to it.

    ``client`` is a ``github.Github`` instance (injected so it can be faked in tests).
    """
    kwargs: dict[str, Any] = {"description": description, "private": private}
    if gitignore:
        kwargs["gitignore_template"] = gitignore
    if license_template:
        kwargs["license_template"] = license_template
    repo = client.get_user().create_repo(name, **kwargs)
    repo.create_file("README.md", "Initial commit: add README", build_readme(name, description))
    return repo


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a GitHub repo with a README.")
    parser.add_argument("name", help="repository name")
    parser.add_argument("-d", "--description", default="", help="repository description")
    parser.add_argument("--private", action="store_true", help="create a private repository")
    parser.add_argument("--gitignore", help="gitignore template, e.g. Python or Node")
    parser.add_argument("--license", dest="license_template", help="license key, e.g. mit")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Set the GITHUB_TOKEN environment variable first.", file=sys.stderr)
        return 1

    from github import Auth, Github, GithubException

    try:
        client = Github(auth=Auth.Token(token))
        repo = create_repository(
            client,
            args.name,
            args.description,
            args.private,
            args.gitignore,
            args.license_template,
        )
    except GithubException as exc:
        message = exc.data.get("message", exc) if isinstance(exc.data, dict) else exc
        print(f"GitHub API error: {message}", file=sys.stderr)
        return 1
    print(f"Created {repo.html_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
