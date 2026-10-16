import os
import subprocess
from pathlib import Path

ENV = {
    **os.environ,
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.com",
}

class ScratchRepo:
    def __init__(self, path: Path):
        self.repo_dir = path
        self.repo_dir.mkdir(parents=True, exist_ok=True)
        self.run("init","-b","main")

    def run(self, *args: str) -> str:
        command_list = ["git", *args]
        return subprocess.run(command_list,cwd=self.repo_dir,
                              env=ENV,capture_output=True,text=True,check=True).stdout.strip()

    def write(self, name: str, content: str) -> None:
        write_path = self.repo_dir/name
        write_path.parent.mkdir(parents=True, exist_ok=True)
        write_path.write_text(content)

    def commit(self, message: str) -> str:    # returns sha
        self.run("add","-A")
        self.run("commit", "-m", message)
        return self.run("rev-parse","HEAD")

    def branch(self, name: str) -> None:
        self.run("branch",name)

    def checkout(self, name: str) -> None:
        self.run("checkout",name)

