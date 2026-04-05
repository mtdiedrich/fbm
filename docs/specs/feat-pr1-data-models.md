# Spec: PR 1 — Data Models

## Goal
Define the core dataclasses (`Card`, `GeneralRuleResult`, `GeneralRule`, `ExactRule`) used by the YGO:FM fusion calculator.

## Current behavior
N/A — new feature.

## Target behavior
`src/fbm/models.py` exports four dataclasses. Each can be instantiated and its fields accessed normally.

### Card
Represents a single card in the game.

```python
Card(
    name="Ice Water",
    atk=1150,
    def_=900,
    g1="Npt",
    g2="Mon",
    primary_type="Aqua",
    secondary_types=["Bugrothian", "Female"],
)
```

Fields:
- `name: str` — card name exactly as it appears in the guide
- `atk: int` — attack points
- `def_: int` — defense points (named with trailing underscore to avoid shadowing `def`)
- `g1: str` — first guardian star abbreviation (e.g. `"Npt"`, `"Mrs"`, `"NUL"`)
- `g2: str` — second guardian star abbreviation
- `primary_type: str` — in-game primary type (e.g. `"Aqua"`, `"Warrior"`, `"Spellcaster"`)
- `secondary_types: list[str]` — zero or more secondary type labels from the guide (e.g. `["Female", "Bugrothian"]`); defaults to empty list

### GeneralRuleResult
Represents one tier result within a general fusion rule.

```python
GeneralRuleResult(
    name="Ice Water",
    atk_threshold=1150,
    conflicts=["Wow Warrior", "Tatsunootoshigo"],
)
```

Fields:
- `name: str` — name of the result card
- `atk_threshold: int` — both fusion materials must have ATK **strictly below** this value for this tier to apply; a value of `0` means no ATK requirement (applies to 0-ATK result cards)
- `conflicts: list[str]` — card names whose own fusion rules take precedence over this result; defaults to empty list

### GeneralRule
Represents a general type-pair fusion rule with one or more ATK tiers.

```python
GeneralRule(
    type1="Female",
    type2="Fish",
    tiers=[
        GeneralRuleResult("Ice Water", 1150, ["Wow Warrior", "Tatsunootoshigo"]),
        GeneralRuleResult("Enchanting Mermaid", 1200, []),
        GeneralRuleResult("Amazon of the Seas", 1300, ["Wow Warrior", "Tatsunootoshigo", "Dark Witch", "Queen of Autumn Leaves"]),
    ],
)
```

Fields:
- `type1: str` — first type label (primary or secondary)
- `type2: str` — second type label
- `tiers: list[GeneralRuleResult]` — tier results ordered ascending by `atk_threshold`; defaults to empty list

### ExactRule
Represents an order-independent exact two-card fusion.

```python
ExactRule(card1="Battle Ox", card2="Dragon Statue", result="Baby Dragon")
```

Fields:
- `card1: str`, `card2: str` — the two fusion material card names (order is arbitrary; lookup is symmetric)
- `result: str` — the result card name

## Files to change

| File | Action | Description |
|------|--------|-------------|
| `src/fbm/models.py` | **Create** | Four dataclasses as described above |
| `tests/test_models.py` | **Create** | Unit tests for instantiation and field access |
| `docs/specs/feat-pr1-data-models.md` | **Create** | This file |

No other files are modified.

## Step-by-step instructions

1. Create `src/fbm/models.py`:
   - Import `dataclass` and `field` from `dataclasses`
   - Define `Card` dataclass with fields: `name`, `atk`, `def_`, `g1`, `g2`, `primary_type`, `secondary_types` (default `field(default_factory=list)`)
   - Define `GeneralRuleResult` dataclass with fields: `name`, `atk_threshold`, `conflicts` (default `field(default_factory=list)`)
   - Define `GeneralRule` dataclass with fields: `type1`, `type2`, `tiers` (default `field(default_factory=list)`)
   - Define `ExactRule` dataclass with fields: `card1`, `card2`, `result`

2. Create `tests/test_models.py` (see Test plan below).

## Test plan

All tests live in `tests/test_models.py`.

| # | Test name | Description | Expected result |
|---|-----------|-------------|-----------------|
| 1 | `test_card_instantiation` | Create a `Card` with all fields | All fields accessible with correct values |
| 2 | `test_card_default_secondary_types` | Create a `Card` without `secondary_types` | `secondary_types == []` |
| 3 | `test_card_secondary_types_not_shared` | Create two separate `Card` objects without `secondary_types`, append to one's list | Lists are independent (default_factory, not mutable default) |
| 4 | `test_general_rule_result_instantiation` | Create a `GeneralRuleResult` with all fields | Fields accessible |
| 5 | `test_general_rule_result_default_conflicts` | Create without `conflicts` | `conflicts == []` |
| 6 | `test_general_rule_instantiation` | Create a `GeneralRule` with two tiers | `type1`, `type2`, `len(tiers) == 2` |
| 7 | `test_general_rule_default_tiers` | Create without `tiers` | `tiers == []` |
| 8 | `test_exact_rule_instantiation` | Create an `ExactRule` | All three fields accessible |
| 9 | `test_models_importable_from_fbm_models` | `from fbm.models import Card, GeneralRuleResult, GeneralRule, ExactRule` | No ImportError |

## Out of scope
- Card data loading (JSON files) — that is PR 2 (`card_db.py`)
- Fusion logic — that is PR 5 (`fusion_engine.py`)
- Any serialization/deserialization helpers
- Type validation at runtime
