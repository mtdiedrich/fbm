# Spec: PR 3 — Exact Fusion Rules Data

## Goal
Encode all 150 exact two-card fusions from section 4 of the fusion guide into `src/fbm/data/exact_rules.json` and validate the data with spot-check tests.

## Current behavior
N/A — new file.

## Target behavior

### JSON format
An array of objects, each with `card1`, `card2`, `result`:

```json
[
  {"card1": "Dark Hole", "card2": "Stain Storm", "result": "Acid Trap Hole"},
  ...
]
```

- Order is canonical but arbitrary — the fusion engine will treat lookups as symmetric (A+B == B+A).
- The array must have exactly **150** entries.
- Card names must match the fusion guide exactly (including apostrophes, hyphens, `#`, spaces).

### Source
All 150 rules come verbatim from section 4 of the fusion guide ("Exact fusion rules"). They are listed in the fusion guide in alphabetical order by result name.

## Files to change

| File | Action | Description |
|------|--------|-------------|
| `src/fbm/data/exact_rules.json` | **Create** | 150 exact fusion rules |
| `tests/test_exact_rules_data.py` | **Create** | Structural validation + 12 spot-checks |
| `docs/specs/feat-pr3-exact-rules.md` | **Create** | This file |

No other files are modified.

## Step-by-step instructions

### 1. Create `src/fbm/data/exact_rules.json`
Encode all 150 rules from guide section 4 in the schema above.

### 2. Create `tests/test_exact_rules_data.py`
See Test plan below. Tests open the file directly with `json.load` — no module dependency.

## Test plan

All tests live in `tests/test_exact_rules_data.py`.

| # | Test name | Description | Expected result |
|---|-----------|-------------|-----------------|
| 1 | `test_file_is_valid_json` | `json.load(file)` succeeds | No exception |
| 2 | `test_total_rule_count` | `len(rules)` | `== 150` |
| 3 | `test_all_entries_have_required_keys` | Every entry has `card1`, `card2`, `result` | All pass |
| 4 | `test_spot_baby_dragon_battle_ox` | `Battle Ox + Dragon Statue = Baby Dragon` present | Found in list |
| 5 | `test_spot_summoned_skull` | `Time Wizard + Embryonic Beast = Summoned Skull` | Found |
| 6 | `test_spot_gaia_dragon_champion` | `Curse of Dragon + Gaia the Fierce Knight = Gaia the Dragon Champion` | Found |
| 7 | `test_spot_musician_king` | `Celtic Guardian + Sonic Maid = Musician King` | Found |
| 8 | `test_spot_red_eyes` | `Red-eyes B. Dragon + Summoned Skull = B. Skull Dragon` | Found |
| 9 | `test_spot_harpie_sisters` | `Elegant Egotist + Harpie Lady = Harpie Lady Sisters` | Found |
| 10 | `test_spot_reaper_of_cards` | `Koumori Dragon + Saggi the Dark Clown = Reaper of the Cards` | Found |
| 11 | `test_spot_witty_phantom_armored` | `Armored Zombie + Wood Clown = Witty Phantom` | Found |
| 12 | `test_spot_dark_energy` | `Yami + Yami = Dark Energy` | Found |
| 13 | `test_no_duplicate_pairs` | Set of frozensets `{card1, card2}` per result has no duplicates across same result | All unique |

## Out of scope
- Loader module for `exact_rules.json` — that is PR 5 (`fusion_engine.py`)
- Symmetric lookup logic — that is PR 5
- Any updates to `cards.json`
