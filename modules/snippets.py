""" Support snippets of code being loaded into the command buffer """
import os
from typing import Dict, List
import pathlib


def get_snippet_list(options: Dict) -> Dict:
    """get the snippets for our servertype"""
    snippet_dict = {}
    path = os.path.join(
        options["HOME"], options["SNIPPETS_PATH"], options["ARGS"].servertype
    )

    if not os.path.exists(path):
        os.makedirs(path)

    snippets = pathlib.Path(path)
    if options["ARGS"].quiet is None:
        print("Loading snippets")
    for snippet in list(snippets.iterdir()):
        _, tail = os.path.split(snippet)
        name, _ = os.path.splitext(tail)
        if options["ARGS"].quiet is None:
            print("\t", name)
        snippet_dict[str(name)] = get_snippet_text(str(snippet))

    return snippet_dict


def get_snippet_text(pathname: str) -> List:
    """Return the text from the snippet file"""
    with open(pathname, "r", encoding="utf-8") as snippet:
        return snippet.readlines()
