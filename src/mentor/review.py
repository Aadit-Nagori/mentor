import typer
from rich import print

app = typer.Typer()

@app.command()
def review():
    print("[red]review:[/red]  ->")