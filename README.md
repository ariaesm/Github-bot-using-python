# GitHub Repo Bot (Python)

Create a new GitHub repository — with a starter README, `.gitignore` and license — in one command, using the GitHub REST API via [PyGithub](https://github.com/PyGithub/PyGithub).

```bash
python github_bot.py my-new-repo -d "Experiments with FastAPI" --gitignore Python --license mit
# Created https://github.com/<you>/my-new-repo
```

## Setup

1. Create a [fine-grained personal access token](https://github.com/settings/personal-access-tokens) with **Administration: read & write** and **Contents: read & write** permissions.
2. Install and configure:

```bash
pip install -r requirements.txt
export GITHUB_TOKEN=github_pat_xxx      # Windows PowerShell: $env:GITHUB_TOKEN="..."
```

The token is read from the environment, never from the code.

## Options

| Option | Description |
| --- | --- |
| `name` | repository name (required) |
| `-d, --description` | repository description |
| `--private` | create a private repository |
| `--gitignore` | gitignore template, e.g. `Python`, `Node` |
| `--license` | license key, e.g. `mit`, `apache-2.0` |

## Tests

The GitHub client is injected, so the tests run offline with a fake:

```bash
pip install pytest
pytest
```

## Ideas

This is the core of a chat-ops bot — the same `create_repository()` function can be called from a Telegram or Slack bot handler.

## License

[MIT](LICENSE)
