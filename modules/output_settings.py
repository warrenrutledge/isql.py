""" allow the user to change behavior and actions of the output """
from typing import Dict, Iterable, List
from prettytable import PLAIN_COLUMNS, MSWORD_FRIENDLY, DEFAULT


def set_method(tokens: List, options: Dict) -> None:
    """allow the user to change the output method"""
    if len(tokens) == 1:
        print(f"OUTPUT_METHOD = {options['OUTPUT_METHOD']}")
    elif tokens[1].lower() == "pretty":
        options["OUTPUT_METHOD"] = "pretty"
    elif tokens[1].lower() == "rich":
        options["OUTPUT_METHOD"] = "rich"
        if options["ARGS"].output is None:
            print("** NOTE: rich output not written to output file **")
    else:
        options["OUTPUT_METHOD"] = "default"


def set_style(tokens: List, options: Dict) -> None:
    """For pretty output only
    Allow the user to change options around the output"""
    lookup = {
        MSWORD_FRIENDLY: "MSWORD_FRIENDLY",
        PLAIN_COLUMNS: "PLAIN_COLUMNS",
        DEFAULT: "DEFAULT",
    }
    if len(tokens) == 1:
        print(f"OUTPUT_STYLE = {lookup[options['OUTPUT_STYLE']]}")
    elif tokens[1].upper() == "MSWORD_FRIENDLY":
        options["OUTPUT_STYLE"] = MSWORD_FRIENDLY
    elif tokens[1].upper() == "PLAIN_COLUMNS":
        options["OUTPUT_STYLE"] = PLAIN_COLUMNS
    else:
        options["OUTPUT_STYLE"] = DEFAULT


def set_align(tokens: List, options: Dict) -> None:
    """For pretty output only
    Allow the user to change column align settings"""
    if len(tokens) == 1:
        print(f"OUTPUT_ALIGN = {options['OUTPUT_ALIGN']}")
    elif tokens[1].upper() == "LEFT" or tokens[1].lower() == "l":
        options["OUTPUT_ALIGN"] = "l"
    elif tokens[1].upper() == "RIGHT" or tokens[1].lower() == "r":
        options["OUTPUT_ALIGN"] = "r"
    else:
        options["OUTPUT_ALIGN"] = "c"


def set_header_caps(tokens: List, options: Dict) -> None:
    """For pretty output only
    Allow use to specify capitalization rules in header"""
    if len(tokens) == 1:
        print(f"HEADER_STYLE = {options['HEADER_STYLE']}")
    elif tokens[1].lower() == "cap":
        options["HEADER_STYLE"] = tokens[1].lower()
    elif tokens[1].lower() == "title":
        options["HEADER_STYLE"] = tokens[1].lower()
    elif tokens[1].lower() == "upper":
        options["HEADER_STYLE"] = tokens[1].lower()
    elif tokens[1].lower() == "lower":
        options["HEADER_STYLE"] = tokens[1].lower()
    else:
        options["HEADER_STYLE"] = None


def toggle(options: Dict, opt_name: str) -> None:
    """Switch True to False or vice versa for this switch"""
    options[opt_name] = not options[opt_name]
    print(f"{opt_name} {options[opt_name]}")


def set_header(_, options: Dict) -> None:
    """Set header options in pretty"""
    toggle(options, "OUTPUT_HEADER")


def set_border(_, options: Dict) -> None:
    """Set border options in pretty"""
    toggle(options, "OUTPUT_BORDER")


def set_csv(_, options: Dict) -> None:
    """Toggle CSV output"""
    toggle(options, "OUTPUT_CSV")


def set_pager(_, options: Dict) -> None:
    """Toggle pager output"""
    toggle(options, "PAGER")


class DispatchTable:
    """This is effectively a switch/case statement"""

    dispatch = {
        ":method": set_method,
        ":style": set_style,
        ":align": set_align,
        ":header": set_header,
        ":border": set_border,
        ":hcaps": set_header_caps,
        ":csv": set_csv,
        ":pager": set_pager,
    }

    def list_keys(self) -> Iterable:
        """list the functions in the dispatch table"""
        return self.dispatch.keys()

    def run(self, cmd: str, opts: Dict, token_array: List) -> None:
        """exec the function pointed to by cmd in dispatch"""
        if cmd in self.dispatch.keys():
            self.dispatch[cmd](token_array, opts)
        else:
            print(f"Unknown output option {' '.join(token_array)}")


def set_options(tokens: List, options: Dict) -> None:
    """Allow interactive changes to settings"""
    dispatch = DispatchTable()
    dispatch.run(tokens[0].lower(), options, tokens)
