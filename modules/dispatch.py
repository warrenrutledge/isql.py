""" base dispatcher for cli of isql.py """
from typing import Dict, List, Iterable
from rich.console import Console
import modules.env_vars as ev
import modules.connection as cn
import modules.helpfile as hf
import modules.process_input as pi
import modules.output_fun as of


console = Console()


def do_reparse(opts: Dict, _) -> None:
    """reparse the isql.cfg file and the command line options"""
    opts = ev.build_options()
    cn.connect(opts)


def do_reset(opts: Dict, _) -> None:
    """reset our buffer and line counter"""
    opts["SQL_BUFFER"] = ""
    opts["LINE_NO"] = 1


def do_connect(opts: Dict, t_list: List) -> None:
    """Reconnect to the database or to a new database"""
    if len(t_list) > 1:  # A database name was passed in so we switch to it
        opts["ARGS"].database = t_list[1]
    cn.connect(opts)


def do_redisplay(opts: Dict, _) -> None:
    """Get the results of the last query and show them again"""
    if opts["PAGER"] is True:
        with console.pager():
            console.print(of.read_cache(opts))
    else:
        if opts["OUTPUT_METHOD"] == "pretty":
            print(of.read_cache(opts))
        else:
            console.print(of.read_cache(opts))


def do_history(opts: Dict, _) -> None:
    """Show the history buffer to the user"""
    for i in range(len(opts["HISTORY"])):
        console.print(f"{i} = {opts['HISTORY'][i]}")


class DispatchTable:
    """This class effectively substitutes as a switch statement
    where the key is the command token and the value is the
    reference to the function to invoke.  We use the same
    arguments to each function (opts, token_array).
    If we fall through the commands, we call process_input
    """

    dispatch = {
        "go": pi.go_function,
        "reparse": do_reparse,
        "reset": do_reset,
        "connect": do_connect,
        "redisplay": do_redisplay,
        "dump": ev.print_opts,
        "help": hf.provide_help,
        "history": do_history,
    }

    def list_keys(self) -> Iterable:
        """provide a list of the entries in the dispatch table"""
        return self.dispatch.keys()

    def run(self, cmd: str, opts: Dict, token_array: List) -> None:
        """execute the command in the dispatch table"""
        if cmd in self.dispatch:
            self.dispatch[cmd](opts, token_array)
        else:
            # Wasn't in the table, so process it
            pi.process_input(opts, token_array)
