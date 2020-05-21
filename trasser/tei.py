from __future__ import annotations

import re

from typing import Callable, List, Optional

from lxml import etree  # nosec


def get_text(
    elt: etree._Element, blacklist: Optional[Callable[[etree._Element], bool]]
) -> str:
    """Extract the text from an XML subtree, with optional element tag blacklisting

    CAVEAT: this collapses all whitespace to a single " "
    
    Note: if you don't actually need a blacklist `etree._Element.itertext` might be a better idea
    """

    if blacklist is None:
        blacklist = lambda x: False  # noqa

    def aux(elt: etree._Element) -> List[str]:
        texts = []
        if not blacklist(elt):  # type: ignore (https://github.com/python/mypy/issues/2608)
            if elt.text is not None and not elt.text.isspace():
                texts.append(elt.text)
            for child in elt:
                texts.extend(aux(child))
        # The tail is not part of the node, so don't ignore it !
        if elt.tail is not None and not elt.tail.isspace():
            texts.append(elt.tail)
        return texts

    texts = aux(elt)
    return re.sub(r"\s+", " ", " ".join(texts).replace("\n", " "))
