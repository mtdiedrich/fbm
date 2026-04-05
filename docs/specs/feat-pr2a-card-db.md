# Spec: PR 2a — CardDB Module

## Goal
Implement the `CardDB` class that loads card data from JSON and provides exact-name lookup and partial-name search; ship a 10-card test fixture and a 3-card skeleton `cards.json`.

## Current behavior
N/A — new feature.

## Target behavior

### JSON format (`cards.json` / fixture)
Each card is a JSON object with these keys:

```json
{
  "name": "Ice Water",
  "atk": 1150,
  "def": 900,
  "g1": "Npt",
  "g2": "Mon",
  "primary_type": "Aqua",
  "secondary_types": ["Bugrothian", "Female"]
}
```

- `"def"` maps to the `Card.def_` field (Python keyword avoidance).
- `"secondary_types"` may be omitted; defaults to `[]`.

### `CardDB` API

```python
from fbm.card_db import CardDB

db = CardDB.load()                         # loads bundled data/cards.json
db = CardDB.load("tests/fixtures/cards_fixture.json")  # custom path

db.get("Ice Water")    # → Card(name="Ice Water", atk=1150, …)
db.get("ice water")    # → same Card (case-insensitive)
db.get("No Such Card") # → None

db.search("water")     # → [Card("Ice Water"), …]  (case-insensitive substring)
db.search("xyzxyz")    # → []

len(db)                # → number of loaded cards
```

## Files to change

| File | Action | Description |
|------|--------|-------------|
| `src/fbm/card_db.py` | **Create** | `CardDB` class |
| `src/fbm/data/__init__.py` | **Create** | Empty — makes `data/` a proper package sub-dir (needed so `Path(__file__)` resolves correctly when installed) |
| `src/fbm/data/cards.json` | **Create** | 3-card skeleton (`Ice Water`, `Celtic Guardian`, `Dragon Zombie`) |
| `tests/fixtures/cards_fixture.json` | **Create** | 10-card fixture used by all `test_card_db.py` tests |
| `tests/test_card_db.py` | **Create** | 11 unit tests |
| `docs/specs/feat-pr2a-card-db.md` | **Create** | This file |

No other files are modified.

## Step-by-step instructions

### 1. Create `src/fbm/data/__init__.py`
Empty file.

### 2. Create `src/fbm/data/cards.json`
Three-card skeleton:
```json
[
  {
    "name": "Ice Water",
    "atk": 1150,
    "def": 900,
    "g1": "Npt",
    "g2": "Mon",
    "primary_type": "Aqua",
    "secondary_types": ["Bugrothian", "Female"]
  },
  {
    "name": "Celtic Guardian",
    "atk": 1400,
    "def": 1200,
    "g1": "Sun",
    "g2": "Urn",
    "primary_type": "Warrior",
    "secondary_types": ["Elf"]
  },
  {
    "name": "Dragon Zombie",
    "atk": 1600,
    "def": 0,
    "g1": "Mon",
    "g2": "Plt",
    "primary_type": "Zombie",
    "secondary_types": ["Dragon"]
  }
]
```

### 3. Create `tests/fixtures/cards_fixture.json`
Ten-card fixture:
```json
[
  {"name":"Ice Water","atk":1150,"def":900,"g1":"Npt","g2":"Mon","primary_type":"Aqua","secondary_types":["Bugrothian","Female"]},
  {"name":"Enchanting Mermaid","atk":1200,"def":900,"g1":"Npt","g2":"Vns","primary_type":"Aqua","secondary_types":["Female"]},
  {"name":"Amazon of the Seas","atk":1300,"def":1400,"g1":"Npt","g2":"Mrs","primary_type":"Aqua","secondary_types":["Female"]},
  {"name":"Celtic Guardian","atk":1400,"def":1200,"g1":"Sun","g2":"Urn","primary_type":"Warrior","secondary_types":["Elf"]},
  {"name":"Fire Reaper","atk":700,"def":500,"g1":"Mrs","g2":"Sun","primary_type":"Zombie","secondary_types":["Pyro"]},
  {"name":"Dragon Zombie","atk":1600,"def":0,"g1":"Mon","g2":"Plt","primary_type":"Zombie","secondary_types":["Dragon"]},
  {"name":"Flame Swordsman","atk":1800,"def":1600,"g1":"Mrs","g2":"Sun","primary_type":"Warrior","secondary_types":["Pyro"]},
  {"name":"Dark Witch","atk":1800,"def":1700,"g1":"Sun","g2":"Npt","primary_type":"Spellcaster","secondary_types":["AngelWinged","FeatherFromMachine","Female"]},
  {"name":"Queen of Autumn Leaves","atk":1800,"def":1500,"g1":"Jpt","g2":"Mon","primary_type":"Plant","secondary_types":["Female"]},
  {"name":"Harpie's Pet Dragon","atk":2000,"def":2500,"g1":"Stn","g2":"Mon","primary_type":"Dragon","secondary_types":[]}
]
```

### 4. Create `src/fbm/card_db.py`

```python
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
                g1=entry["g1"],
                g2=entry["g2"],
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
```

### 5. Create `tests/test_card_db.py`
See Test plan below.

## Test plan

All tests live in `tests/test_card_db.py`. All use `FIXTURE_PATH = Path(__file__).parent / "fixtures" / "cards_fixture.json"`.

| # | Test name | Description | Expected result |
|---|-----------|-------------|-----------------|
| 1 | `test_load_returns_carddb` | `CardDB.load(fixture)` | Returns a `CardDB` instance |
| 2 | `test_len_matches_fixture` | `len(db)` | `== 10` |
| 3 | `test_get_known_card` | `db.get("Ice Water")` | Not None; `atk == 1150`, `def_ == 900` |
| 4 | `test_get_returns_card_instance` | `db.get("Celtic Guardian")` | Is a `Card` instance |
| 5 | `test_get_unknown_card` | `db.get("No Such Card")` | `None` |
| 6 | `test_get_case_insensitive` | `db.get("ice water") == db.get("Ice Water")` | `True` |
| 7 | `test_get_secondary_types` | `db.get("Dark Witch").secondary_types` | Contains `"Female"` and `"AngelWinged"` |
| 8 | `test_search_partial_match` | `db.search("water")` | Result list contains `"Ice Water"` |
| 9 | `test_search_no_match` | `db.search("xyznonexistent")` | `== []` |
| 10 | `test_search_case_insensitive` | `db.search("ICE WATER") == db.search("ice water")` | Equal, non-empty |
| 11 | `test_load_default_path` | `CardDB.load()` (no args) | Returns `CardDB` without error |

## Out of scope
- Populating `cards.json` with the full card list — that is PR 2b
- Any write/save operations on `CardDB`
- Type validation on JSON values
- Fuzzy matching (only exact prefix/substring)
- Serialization back to JSON
