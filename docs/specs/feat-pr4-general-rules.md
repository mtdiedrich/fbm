# Spec: feat/pr4-general-rules

## Goal

Encode all general fusion rules derived from the Yugipedia FM fusion pages (001–722) as
`general_rules.json`, and resolve the two open model design issues from PR 1 that were
blocking this work.

## Model Design Changes (prerequisites)

### Card model: replace `g1`/`g2` with `groups: list[str]`

**Problem**: Each card in FMR can belong to 2–4 distinct fusion groups, but the current
`Card` dataclass has only `g1: str` and `g2: str`.

**Change**:
```python
# BEFORE
@dataclass
class Card:
    name: str; atk: int; def_: int; g1: str; g2: str; primary_type: str
    secondary_types: list[str] = field(default_factory=list)

# AFTER
@dataclass
class Card:
    name: str; atk: int; def_: int; groups: list[str]
    primary_type: str
    secondary_types: list[str] = field(default_factory=list)
```

### GeneralRule model: replace tier system with flat `result` field

**Problem**: The `tiers: list[GeneralRuleResult]` structure requires ATK threshold data
that is not yet available. The `GeneralRuleResult` class is over-engineered for the
current data state.

**Change**:
```python
# BEFORE
@dataclass
class GeneralRuleResult:
    name: str; atk_threshold: int; conflicts: list[str] = ...

@dataclass
class GeneralRule:
    type1: str; type2: str; tiers: list[GeneralRuleResult] = ...

# AFTER (GeneralRuleResult removed)
@dataclass
class GeneralRule:
    type1: str; type2: str; result: str
```

Multiple entries with the same `(type1, type2)` pair represent different ATK tiers; the
order in the JSON file is low-to-high (weakest result first). ATK threshold values can be
added as a separate optional field in a future PR once the card ATK data is complete.

## Target Behavior

- `src/fbm/data/general_rules.json` exists and contains exactly **74** entries.
- Each entry has the shape `{"type1": str, "type2": str, "result": str}`.
- `type1` and `type2` are canonical FMR fusion group names.
- `Card.groups` is a `list[str]`; `Card.g1` and `Card.g2` are gone.
- `GeneralRule` has `(type1, type2, result)`; `GeneralRuleResult` is gone.
- All 35+ existing tests pass.

## Canonical FMR Group Names Used

The following group name strings are used in `type1`/`type2` fields:

| JSON string | Meaning |
|---|---|
| `"Aqua"` | Aqua-type water creatures |
| `"Beast"` | Beast-type monsters |
| `"Black Magic (Mercury)"` | Dark spellcaster cards (Mercury planet group) |
| `"Dinosaur"` | Dinosaur-type monsters |
| `"Dragon"` | Dragon-type monsters |
| `"Egg"` | Egg-group monsters (Monster Egg, Gorgon Egg, etc.) |
| `"Elf"` | Elf-type monsters |
| `"Fairy"` | Fairy-type monsters |
| `"Female"` | Female-group monsters |
| `"Fiend"` | Fiend-type monsters (general) |
| `"Fiend Magic (Moon)"` | Dark fiend/evil cards (Moon planet group) |
| `"Fire (Mars)"` | Pyro/Fire-type cards (Mars planet group) |
| `"Fish"` | Fish-type monsters |
| `"Harpie"` | Harpie-type monsters |
| `"Insect"` | Insect-type monsters |
| `"Jar"` | Jar/Pot-group monsters (Ancient Jar, Morphing Jar, etc.) |
| `"Machine"` | Machine-type monsters |
| `"Plant"` | Plant-type monsters |
| `"Reptile"` | Reptile-type monsters |
| `"Rock"` | Rock-type monsters |
| `"Spellcaster"` | Spellcaster-type monsters |
| `"Thunder (Pluto)"` | Thunder-type cards (Pluto planet group) |
| `"Turtle"` | Turtle-type monsters |
| `"Warrior"` | Warrior-type monsters |
| `"Water (Neptune)"` | Water/Neptune-group monsters |
| `"Winged Beast"` | Winged Beast-type monsters |
| `"Zombie"` | Zombie-type monsters |

## Files Changed

| File | Action | Summary |
|---|---|---|
| `src/fbm/models.py` | Modify | Remove `GeneralRuleResult`; replace `g1`/`g2` in `Card` with `groups`; replace `tiers` in `GeneralRule` with `result` |
| `tests/test_models.py` | Modify | Remove `GeneralRuleResult` tests; update `Card` and `GeneralRule` tests |
| `tests/fixtures/cards_fixture.json` | Modify | Replace `g1`/`g2` with `groups` array on all 10 fixture cards |
| `src/fbm/data/cards.json` | Modify | Replace `g1`/`g2` with `groups` array on 3 skeleton cards |
| `src/fbm/data/general_rules.json` | Create | 75 general rule entries |
| `tests/test_general_rules_data.py` | Create | Validation tests for general_rules.json |

## general_rules.json — Complete Entry List (75 entries)

Entries are sorted by `(type1, type2, result)` in the JSON file.

| type1 | type2 | result |
|---|---|---|
| Beast | Female | Nekogal #2 |
| Beast | Fiend | Mystical Sheep #1 |
| Beast | Fish | Rare Fish |
| Beast | Machine | Dice Armadillo |
| Beast | Machine | Giga-tech Wolf |
| Beast | Warrior | Tiger Axe |
| Black Magic (Mercury) | Machine | Disk Magician |
| Dinosaur | Machine | Cyber Saurus |
| Dinosaur | Zombie | Great Mammoth of Goldfine |
| Dragon | Aqua | Kairyu-Shin |
| Dragon | Aqua | Spike Seadra |
| Dragon | Fiend | Koumori Dragon |
| Dragon | Machine | Metal Dragon |
| Dragon | Warrior | D. Human |
| Dragon | Warrior | Dragon Statue |
| Dragon | Warrior | Dragoness the Wicked Knight |
| Dragon | Warrior | Sword Arm of Dragon |
| Dragon | Zombie | Curse of Dragon |
| Dragon | Zombie | Dragon Zombie |
| Dragon | Zombie | Skelgon |
| Egg | Female | Winged Egg of New Life |
| Elf | Black Magic (Mercury) | Dark Elf |
| Elf | Fairy | Mystical Elf |
| Elf | Fiend Magic (Moon) | Dark Elf |
| Elf | Warrior | Celtic Guardian |
| Fiend | Plant | Rose Spectre of Dunn |
| Fiend | Winged Beast | Whiptail Crow |
| Fiend Magic (Moon) | Plant | Darkworld Thorns |
| Fire (Mars) | Beast | Flame Cerebrus |
| Fire (Mars) | Plant | Firegrass |
| Fire (Mars) | Rock | Dissolverock |
| Fire (Mars) | Warrior | Charubin the Fire Knight |
| Fire (Mars) | Warrior | Flame Swordsman |
| Fire (Mars) | Zombie | Fire Reaper |
| Fire (Mars) | Zombie | Flame Ghost |
| Fish | Beast | Marine Beast |
| Fish | Female | Amazon of the Seas |
| Fish | Machine | Misairuzame |
| Fish | Warrior | Wow Warrior |
| Fish | Zombie | Corroding Shark |
| Insect | Insect | Kwagar Hercules |
| Jar | Spellcaster | Ushi Oni |
| Machine | Aqua | Amphibious Bugroth |
| Machine | Warrior | Cyber Soldier |
| Plant | Beast | Flower Wolf |
| Plant | Dragon | B. Dragon Jungle King |
| Plant | Female | Queen of Autumn Leaves |
| Plant | Warrior | Bean Soldier |
| Reptile | Plant | Snakeyashi |
| Rock | Dragon | Stone D. |
| Rock | Female | Mystical Sand |
| Rock | Warrior | Minomushi Warrior |
| Rock | Zombie | Stone Ghost |
| Thunder (Pluto) | Aqua | Bolt Escargot |
| Thunder (Pluto) | Beast | Tripwire Beast |
| Thunder (Pluto) | Dragon | Thunder Dragon |
| Thunder (Pluto) | Dragon | Twin-headed Thunder Dragon |
| Thunder (Pluto) | Reptile | Electric Lizard |
| Thunder (Pluto) | Spellcaster | Kaminari Attack |
| Thunder (Pluto) | Spellcaster | The Immortal of Thunder |
| Turtle | Beast | Turtle Tiger |
| Turtle | Fire (Mars) | Giant Turtle Who Feeds on Flames |
| Turtle | Rock | Boulder Tortoise |
| Turtle | Spellcaster | 30,000-Year White Turtle |
| Turtle | Winged Beast | Turtle Bird |
| Warrior | Insect | Cockroach Knight |
| Winged Beast | Fire (Mars) | Crimson Sunbird |
| Winged Beast | Fire (Mars) | Mavelus |
| Zombie | Beast | Shadow Specter |
| Zombie | Plant | Pumpking the King of Ghosts |
| Zombie | Plant | Wood Remains |
| Zombie | Spellcaster | Magical Ghost |
| Zombie | Warrior | Armored Zombie |
| Zombie | Warrior | Zombie Warrior |

> **Note**: Entries for `Elf + Black Magic (Mercury) → Dark Elf` and
> `Elf + Fiend Magic (Moon) → Dark Elf` are included based on analysis of the material
> card lists in the Yugipedia data; the exact group boundary between those two dark groups
> requires verification against game ROMs or additional Yugipedia data.

## Test Plan (`tests/test_general_rules_data.py`)

| # | Test name | Expected result |
|---|---|---|
| 1 | `test_general_rules_file_exists` | `general_rules.json` path exists |
| 2 | `test_general_rules_is_valid_json` | File parses without error |
| 3 | `test_general_rules_count` | `len(rules) == 75` |
| 4 | `test_each_rule_has_required_keys` | Every entry has `type1`, `type2`, `result` |
| 5 | `test_no_extra_keys` | No entry has keys other than the three |
| 6 | `test_all_values_are_nonempty_strings` | All three fields are non-empty `str` |
| 7 | `test_spot_check_flame_swordsman` | `{"type1":"Fire (Mars)","type2":"Warrior","result":"Flame Swordsman"}` present |
| 8 | `test_spot_check_koumori_dragon` | `{"type1":"Dragon","type2":"Fiend","result":"Koumori Dragon"}` present |
| 9 | `test_spot_check_turtle_spellcaster` | `{"type1":"Turtle","type2":"Spellcaster","result":"30,000-Year White Turtle"}` present |
| 10 | `test_spot_check_dark_elf_fiend_magic_moon` | `{"type1":"Elf","type2":"Fiend Magic (Moon)","result":"Dark Elf"}` present |
| 11 | `test_no_duplicate_entries` | No (type1, type2, result) triple appears twice |

## Updated model tests (`tests/test_models.py`)

Remove: `test_general_rule_result_instantiation`, `test_general_rule_result_default_conflicts`.
Remove: `test_general_rule_instantiation` (uses tiers), `test_general_rule_default_tiers`.

Replace with:
```python
def test_general_rule_instantiation():
    rule = GeneralRule(type1="Fire (Mars)", type2="Warrior", result="Flame Swordsman")
    assert rule.type1 == "Fire (Mars)"
    assert rule.type2 == "Warrior"
    assert rule.result == "Flame Swordsman"

def test_general_rule_importable():
    from fbm.models import GeneralRule  # noqa: F401
```

Also replace Card tests that use `g1`/`g2` with `groups`.

## Out of Scope

- ATK threshold data for distinguishing tiers within the same `(type1, type2)` pair
- Spell/trap card fusions (Legendary Sword, Raigeki, etc.)
- Full `cards.json` population (PR 2b)
- Fusion engine logic (PR 5)
- Glitch fusions
- Specific-card rules (e.g., "Harpie Lady + Dragon", "Time Wizard + Dragon")
