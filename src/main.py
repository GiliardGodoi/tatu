
import click
import PyPDF2
from pathlib import Path
from rich.console import Console
from rich.traceback import install

install()

console = Console()

@click.group()
def cli():
    pass

@cli.command()
@click.argument('filename', type=click.Path(exists=True, dir_okay=True), nargs=-1)
@click.option('-o', '--output', default='tatu.pdf', type=str)
def join(filename, output):

    if not output.endswith('.pdf'): output = f'{output}.pdf'

    print(type(filename), filename, output)

@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-o', '--output', default="tatu (%d).pdf", type=str)
def split(filename, output):

    print(type(filename), filename)
    base_dir = Path(output)
    base_dir = base_dir if base_dir.is_dir() else Path('.')
    base_name = "tatu (%d).pdf"

    with open(filename, 'rb') as rbfile:
        pdf_reader = PyPDF2.PdfFileReader(rbfile)

        for index in range(pdf_reader.numPages):
            output_file_name = base_dir / Path(base_name % index)
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(pdf_reader.getPage(index))
            with open(output_file_name, 'wb') as wbfile:
                pdf_writer.write(wbfile)

@cli.command()
def retrive(source, dest):
    pass

if __name__ == "__main__":
    cli()
