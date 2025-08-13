import sys
from typing import Annotated
import typer


app = typer.Typer(
    name="pascal_to_kebab",
    help="[Converts class name form pascal to kebab].",
)


def convert_pascal_to_kebab(input_data: str) -> str:
    result = ""
    for i, ch in enumerate(input_data):
        if ch.isupper() and i != 0:
            result += "-"
        result += ch.lower()
    return result


@app.command()
def main(
    input_argument: Annotated[
        str,
        typer.Argument(
            help="[Help text for the command-line argument].",
            show_default=False,
        ),
    ]
):
    try:
        result = convert_pascal_to_kebab(input_argument)
    
        typer.echo(result)
        
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    app()