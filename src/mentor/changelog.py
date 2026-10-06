import typer
from rich import print

app = typer.Typer()

@app.command()
def changelog():
    print("[blue]changelog:[/blue]  ->")