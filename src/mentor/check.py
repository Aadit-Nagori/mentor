import typer
from rich import print

app = typer.Typer()

@app.command()
def check():
    print("[green]check:[/green]  ->")