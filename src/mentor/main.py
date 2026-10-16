from importlib.metadata import version as get_version
from typing import Annotated

import typer

from .changelog import app as changelog_app
from .check import app as check_app
from .review import app as review_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(changelog_app)
app.add_typer(check_app)
app.add_typer(review_app)


def _version_callback(value: bool) -> None:
    if value:
        print(f"mentor version: {get_version('mentor')}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version", "-v",
            callback=_version_callback,
            is_eager=True,
            help="Show the version and exit.",
        ),
    ] = False,
) -> None:
    pass


if __name__ == "__main__":
    app()
