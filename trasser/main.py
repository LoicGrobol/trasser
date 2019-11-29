import click
import lxml  # nosec
import lxml.etree  # nosec


@click.command()
@click.argument('inpt', nargs=-1)
def main_entry_point(inpt):
    """Convert Transcriber files to raw text"""
    for f in inpt:
        tree = lxml.etree.parse(f)  # nosec
        for e in tree.iter():
            for t in (e.text, e.tail):
                if t is not None and not t.isspace():
                    click.echo(t.strip())


if __name__ == '__main__':
    main_entry_point()
