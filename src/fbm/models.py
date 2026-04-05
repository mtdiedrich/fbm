from dataclasses import dataclass, field


@dataclass
class Card:
    name: str
    atk: int
    def_: int
    groups: list[str]
    primary_type: str
    secondary_types: list[str] = field(default_factory=list)


@dataclass
class GeneralRule:
    type1: str
    type2: str
    result: str


@dataclass
class ExactRule:
    card1: str
    card2: str
    result: str
