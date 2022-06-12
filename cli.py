"""CLI Module of bmpy

Provides simple functions that encapsulate the cli functionality.
I chose to avoid argparse, docopt, click etc. since I find them confusing sometimes.
Also my usecase is quite simple, so those modules felt overkill.

The final CLI should provide the following functions:
    - adding bookmarks via "-a" or "--add" followed by the name of the bookmark, the url of the bookmark and categories for that bookmark
        -> bmpy -a "Name of the bookmark" "url.to.the.bookmark" # example tutorial
    - deleting bookmarks via "-d" or "--delete" followed by a keyword to look for. If the specified keyword is unique in the database only a 
    confirmation prompt will be shown else a list of matching bookmarks will show up.
        -> bmpy -d "Name"
"""
from sys import argv
from typing import Callable
from bmpy_exceptions import (
    InvalidCLIOperationException,
    InvalidHelpTargetException,
    InvalidListTargetException,
    InvalidSearchTargetException,
    TooFewAddArgumentsException,
    TooFewArgumentsException,
    TooFewDeleteArguments,
    TooFewFindArgumentsException,
)
from bmpy_types import (
    CLI_OPERATION,
    AddArguments,
    DeleteArguments,
    DeleteTarget,
    EditArguments,
    FindArguments,
    HelpArguments,
    HelpTarget,
    ListArguments,
    ListTarget,
    ParsedArguments,
    SearchTarget,
)


class SearchFlags:
    ID = ["-i", "--id"]
    NAME = ["-n", "--name"]
    URL = ["-u", "--url"]
    CATEGORY = ["-c", "--category"]


class CLIFlags:
    ADD = ["-a", "--add"]
    EDIT = ["-e", "--edit"]
    FIND = ["-f", "--find"]
    LIST = ["-l", "--list"]
    DELETE = ["-d", "--delete"]
    HELP = ["-h", "--help"]


def parse_add(args: list[str]) -> AddArguments:
    """Parses the cli arguments into a dataclass to make further work with the data easier
    Example:
        bmpy --add "Name of the bookmark" "url.of.the.bookmark" -cooking -healthy
    Args:
        args (list[str]): "raw" cli input arguments

    Returns:
        AddArguments: Dataclass wrapping arguments for add operation
    """
    if len(args) < 2:
        raise TooFewAddArgumentsException(f"Not enough arguments provided: {args=}")

    categories = [arg[1:] for arg in args if arg.startswith("-")]
    return AddArguments(name=args[0], url=args[1], categories=categories)


def parse_edit(args: list[str]) -> EditArguments:
    ...


def get_search_type(flag: str) -> SearchTarget:
    if flag in SearchFlags.ID:
        return SearchTarget.ID
    elif flag in SearchFlags.NAME:
        return SearchTarget.NAME
    elif flag in SearchFlags.URL:
        return SearchTarget.URL
    elif flag in SearchFlags.CATEGORY:
        return SearchTarget.CATEGORY
    else:
        raise InvalidSearchTargetException(f"Specified search flag invalid: {flag=}")


def parse_find(args: list[str]) -> FindArguments:
    if len(args) < 1:
        raise TooFewFindArgumentsException(f"Not enough arguments provided: {args=}")

    if len(args) == 1:
        return FindArguments(keyword=args[0], search_target=SearchTarget.ANY)

    search_target = get_search_type(args[1])
    return FindArguments(keyword=args[0], search_target=search_target)


def get_list_type(flag: str) -> ListTarget:
    if flag in SearchFlags.NAME:
        return ListTarget.NAME
    elif flag in SearchFlags.URL:
        return ListTarget.URL
    elif flag in SearchFlags.CATEGORY:
        return ListTarget.CATEGORY
    else:
        raise InvalidListTargetException(f"Specified list flag invalid: {flag=}")


def parse_list(args: list[str]) -> ListArguments:
    if len(args) == 0:
        return ListArguments(list_target=ListTarget.ALL)

    list_type = get_list_type(args[0])
    return ListArguments(list_target=list_type)


def get_delete_type(flag: str) -> DeleteTarget:
    ...


def parse_delete(args: list[str]) -> DeleteArguments:
    if len(args) < 2:
        raise TooFewDeleteArguments(f"Not enough arguments provided: {args=}")

    if len(args) == 2:
        return DeleteArguments(
            keyword=args[0],
        )


def get_help_type(flag: str) -> HelpTarget:
    if flag in CLIFlags.ADD:
        return HelpTarget.ADD
    elif flag in CLIFlags.DELETE:
        return HelpTarget.DELETE
    elif flag in CLIFlags.EDIT:
        return HelpTarget.EDIT
    elif flag in CLIFlags.FIND:
        return HelpTarget.FIND
    elif flag in CLIFlags.LIST:
        return HelpTarget.LIST
    else:
        raise InvalidHelpTargetException(f"Specified help flag invalid: {flag=}")


def parse_help(args: list[str]) -> HelpArguments:
    if len(args) == 0:
        return HelpArguments(operation=CLI_OPERATION.HELP)
    help_type = get_help_type(args[0])
    return HelpArguments(operation=help_type)


def get_operation(
    cli_input: list[str],
) -> tuple[CLI_OPERATION, Callable[[list[str]], ParsedArguments]]:
    op = cli_input[0]
    args = cli_input[1:]

    if op in CLIFlags.ADD:
        return CLI_OPERATION.ADD, parse_add(args)
    elif op in CLIFlags.EDIT:
        return CLI_OPERATION.EDIT, parse_edit(args)
    elif op in CLIFlags.FIND:
        return CLI_OPERATION.FIND, parse_find(args)
    elif op in CLIFlags.LIST:
        return CLI_OPERATION.LIST, parse_list(args)
    elif op in CLIFlags.DELETE:
        return CLI_OPERATION.DELETE, parse_delete(args)
    elif op in CLIFlags.HELP:
        return CLI_OPERATION.HELP, parse_help(args)
    else:
        raise InvalidCLIOperationException(
            f"Specified operation={op} is not a valid option."
        )


def parse_cli():
    if len(argv) == 1:
        raise TooFewArgumentsException("You didn't specify an operation")

    cli_input = argv[1:]

    operation, parsed_arguments = get_operation(cli_input=cli_input)
    print(parsed_arguments)


parse_cli()
