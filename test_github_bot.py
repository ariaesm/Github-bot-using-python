from types import SimpleNamespace

import github_bot


class FakeRepo:
    html_url = "https://github.com/me/demo"

    def __init__(self):
        self.files = {}

    def create_file(self, path, message, content):
        self.files[path] = (message, content)


class FakeUser:
    def __init__(self):
        self.calls = []
        self.repo = FakeRepo()

    def create_repo(self, name, **kwargs):
        self.calls.append((name, kwargs))
        return self.repo


def test_build_readme_includes_name_and_description():
    readme = github_bot.build_readme("demo", "A test repo")
    assert readme.startswith("# demo\n")
    assert "A test repo" in readme


def test_create_repository_passes_options_and_adds_readme():
    user = FakeUser()
    client = SimpleNamespace(get_user=lambda: user)
    repo = github_bot.create_repository(client, "demo", "desc", True, "Python", "mit")
    assert user.calls == [
        (
            "demo",
            {
                "description": "desc",
                "private": True,
                "gitignore_template": "Python",
                "license_template": "mit",
            },
        )
    ]
    assert "README.md" in repo.files


def test_main_requires_token(monkeypatch, capsys):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    assert github_bot.main(["demo"]) == 1
    assert "GITHUB_TOKEN" in capsys.readouterr().err
