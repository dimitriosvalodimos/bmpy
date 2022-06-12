from dataclasses import dataclass
from enum import Enum, auto
from sre_constants import CATEGORY


class CLI_OPERATION(Enum):
    ADD = auto()
    EDIT = auto()
    FIND = auto()
    LIST = auto()
    DELETE = auto()
    HELP = auto()


class EditTarget(Enum):
    NAME = auto()
    URL = auto()
    CATEGORY = auto()


class SearchTarget(Enum):
    ID = auto()
    NAME = auto()
    URL = auto()
    CATEGORY = auto()
    ANY = auto()


class ListTarget(Enum):
    NAME = auto()
    URL = auto()
    CATEGORY = auto()
    ALL = auto()


class DeleteTarget(Enum):
    NAME = auto()
    URL = auto()
    CATEGORY = auto()
    ANY = auto()


@dataclass
class HelpTarget(CLI_OPERATION):
    pass


@dataclass
class AddArguments:
    name: str
    url: str
    categories: list[str]


@dataclass
class EditArguments:
    keyword: str
    edit_target: EditTarget
    change_to: str


@dataclass
class FindArguments:
    keyword: str
    search_target: SearchTarget


@dataclass
class ListArguments:
    list_target: ListTarget


@dataclass
class DeleteArguments:
    keyword: str
    delete_target: DeleteTarget
    hard_delete: bool


@dataclass
class HelpArguments:
    operation: CLI_OPERATION


ParsedArguments = (
    AddArguments
    | EditArguments
    | FindArguments
    | ListArguments
    | DeleteArguments
    | HelpArguments
)
