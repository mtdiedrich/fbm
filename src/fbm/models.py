from dataclasses import dataclass, field


@dataclass
class Card:
    name: str
    atk: int
    def_: int
    g1: str
    g2: str
    primary_type: str
    secondary_types: list[str] = field(default_factory=list)


@dataclass
class GeneralRuleResult:
    name: str
    atk_threshold: int
    conflicts: list[str] = field(default_factory=list)


@dataclass
class GeneralRule:
    type1: str
    type2: str
    tiers: list[GeneralRuleResult] = field(default_factory=list)


@dataclass
class ExactRule:
    card1: str
    card2: str
    result: str
