
import contextlib
from pathlib import Path

import click
import PyPDF2
from rich.console import Console
from rich.traceback import install

install()

console = Console()

@click.group()
def cli():
    pass

@cli.command()
@click.argument('source', type=click.Path(exists=True, dir_okay=True), nargs=-1)
@click.option('-o', '--output', default='tatu.pdf', type=str)
def merge(source, output):

    source = Path(source[0])
    if not source.is_dir():
        raise RuntimeError('source is not a directory!')

    pdf_files = [f for f in source.glob("*.pdf") ]

    if not pdf_files:
        raise RuntimeError("No input pdf files!")

    with contextlib.ExitStack() as stack:
        files = [ stack.enter_context(open(pdf, 'rb')) for pdf in pdf_files]
        pdf_merger = PyPDF2.PdfFileMerger()
        for f in files:
            pdf_merger.append(f)

        output = output if output.endswith('.pdf') else f'{output}.pdf'
        with open(output, 'wb') as f:
            pdf_merger.write(f)

@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-f', '--base-folder', default=".", type=str)
@click.option('-n', '--base-name', default="tatu (%d).pdf", type=str)
def split(filename, base_folder, base_name):

    print(type(filename), filename)
    base_folder = Path(base_folder)
    base_folder = base_folder if base_folder.is_dir() else Path('.')
    base_name = "tatu (%d).pdf"

    with open(filename, 'rb') as rbfile:

        pdf_reader = PyPDF2.PdfFileReader(rbfile)

        for index in range(pdf_reader.numPages):
            output_file_name = base_folder / Path(base_name % index)
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(pdf_reader.getPage(index))
            with open(output_file_name, 'wb') as wbfile:
                pdf_writer.write(wbfile)

@cli.command()
def cut():
    pass

@cli.command()
def retrive(source, dest):
    pass

if __name__ == "__main__":
    cli()
