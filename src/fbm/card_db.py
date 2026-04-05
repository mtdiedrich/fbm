from __future__ import annotations

import json
from pathlib import Path

from fbm.models import Card

_DEFAULT_PATH = Path(__file__).parent / "data" / "cards.json"


class CardDB:
    def __init__(self, cards: list[Card]) -> None:
        self._cards = cards
        self._index: dict[str, Card] = {c.name.lower(): c for c in cards}

    @classmethod
    def load(cls, path: Path | str | None = None) -> CardDB:
        resolved = Path(path) if path is not None else _DEFAULT_PATH
        with resolved.open(encoding="utf-8") as fh:
            data = json.load(fh)
        cards = [
            Card(
                name=entry["name"],
                atk=entry["atk"],
                def_=entry["def"],
                groups=entry.get("groups", []),
                primary_type=entry["primary_type"],
                secondary_types=entry.get("secondary_types", []),
            )
            for entry in data
        ]
        return cls(cards)

    def get(self, name: str) -> Card | None:
        return self._index.get(name.lower())

    def search(self, partial: str) -> list[Card]:
        needle = partial.lower()
        return [c for c in self._cards if needle in c.name.lower()]

    def __len__(self) -> int:
        return len(self._cards)
