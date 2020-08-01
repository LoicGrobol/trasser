import click
import lxml  # nosec
import lxml.etree  # nosec

from typing import List, Optional

import trasser.tei


TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"

NSMAP = {"tei": TEI[1:-1], "xml": XML[1:-1]}


@click.group()
def cli():
    pass


@cli.command()
@click.argument('inpt', nargs=-1)
def tsv(inpt):
    """Convert Transcriber files to raw text"""
    for f in inpt:
        tree = lxml.etree.parse(f)  # nosec
        for e in tree.iter():
            for t in (e.text, e.tail):
                if t is not None and not t.isspace():
                    click.echo(t.strip())


@cli.command()
@click.argument('inpt', nargs=-1)
@click.option("--attr-blacklist", help="A comma-separated list of attr:value to ignore")
@click.option(
    "--lines-xpath",
    default=".//text/body//p|.//text/body//l|.//text/body//head",
    help="An xpath expression matching the individual lines to extract",
)
@click.option("--tags-blacklist", help="A comma-separated list of tags to ignore")
def tei(
    inpt: List[str],
    lines_xpath: str,
    tags_blacklist: Optional[str],
    attr_blacklist: Optional[str],
):
    """Convert TEI files to raw text"""
    if tags_blacklist is None:
        blacklist_set = set()
    else:
        blacklist_set = set(tags_blacklist.split(","))

    def blacklist(elt):
        return elt.tag in blacklist_set

    if attr_blacklist is None:
        forbidden_attrs = None
    else:
        forbidden_attrs = [tuple(p.split(":")) for p in attr_blacklist.split(",")]

    for f in inpt:
        tree = lxml.etree.parse(f)  # nosec
        for e in tree.xpath(lines_xpath, namespaces=NSMAP):
            if forbidden_attrs is not None:
                if any(
                    p.tag in blacklist_set
                    or any(p.get(a) == v for a, v in forbidden_attrs)
                    for p in e.iterancestors()
                ):
                    continue
            click.echo(trasser.tei.get_text(e, blacklist))


@cli.command()
@click.argument('inpt', nargs=-1)
def conll(inpt):
    """Convert conll files to raw text"""
    for f in inpt:
        with open(f) as in_stream:
            for l in in_stream:
                if l.startswith("# text = "):
                    click.echo(l[9:].strip())


if __name__ == '__main__':
    cli()
