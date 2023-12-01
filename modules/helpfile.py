""" Module to display help text """
import os
from typing import Dict, List
from rich.console import Console
from rich.markdown import Markdown

console = Console()


def display_help(helpfile: str) -> None:
    """Read the file and print the contents to screen"""
    with open(helpfile, "r") as helpinfo:
        for line in helpinfo:
            out = Markdown(line[:-1])
            console.print(out, style="yellow")


def get_topics(options: Dict) -> Dict:
    """Get the list of help topics"""
    dirlist = os.listdir(f"{options['CODE_DIR']}/help")
    topics = {}
    for file in sorted(dirlist):
        if file[-3:] == ".md":
            topics[file[:-3]] = f"{options['CODE_DIR']}/help/{file}"

    return topics


def provide_help(options: Dict, tokens: List) -> None:
    """base routine to parse help command input"""
    topics = get_topics(options)
    if len(tokens) == 1:
        display_help(f"{options['CODE_DIR']}/help/help.md")
    elif tokens[1] == "topics":
        console.print("Help topics:", end="", style="yellow")
        for topic in topics:
            console.print(f" {topic}", end="", style="yellow")
        print()
    else:
        if tokens[1] in topics:
            display_help(topics[tokens[1]])
        else:
            console.print(f"Unknown topic: {tokens[1].strip()}", style="yellow")
