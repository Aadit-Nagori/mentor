import typer
from rich import print

app = typer.Typer()

@app.command()
def check() -> None:
    print("[green]check:[/green]  ->")
