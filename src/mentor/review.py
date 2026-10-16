import typer
from rich import print

app = typer.Typer()

@app.command()
def review() -> None:
    print("[red]review:[/red]  ->")
