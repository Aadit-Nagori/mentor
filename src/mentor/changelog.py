import typer
from rich import print

app = typer.Typer()

@app.command()
def changelog() -> None:
    print("[blue]changelog:[/blue]  ->")
