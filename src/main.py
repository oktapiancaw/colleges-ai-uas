import typer
from .core import base, analytics

app = typer.Typer(pretty_exceptions_show_locals=False)
app.add_typer(base.app, name="base", help="basic usage")
app.add_typer(analytics.app, name="analytics", help="Analytics usage")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"Base Engine")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
