import json
from pathlib import Path

GENERAL_RULES_PATH = (
    Path(__file__).parent.parent / "src" / "fbm" / "data" / "general_rules.json"
)
EXPECTED_COUNT = 74


def test_general_rules_file_exists():
    assert GENERAL_RULES_PATH.exists()


def test_general_rules_is_valid_json():
    with GENERAL_RULES_PATH.open(encoding="utf-8") as f:
        rules = json.load(f)
    assert isinstance(rules, list)


def test_general_rules_count():
    with GENERAL_RULES_PATH.open(encoding="utf-8") as f:
        rules = json.load(f)
    assert len(rules) == EXPECTED_COUNT, (
        f"Expected {EXPECTED_COUNT} rules, got {len(rules)}"
    )


def test_each_rule_has_required_keys():
    with GENERAL_RULES_PATH.open(encoding="utf-8") as f:
        rules = json.load(f)
    for i, rule in enumerate(rules):
        for key in ("type1", "type2", "result"):
            assert key in rule, f"Rule {i} missing key '{key}': {rule}"


def test_no_extra_keys():
    allowed = {"type1", "type2", "result"}
    with GENERAL_RULES_PATH.open(encoding="utf-8") as f:
        rules = json.load(f)
    for i, rule in enumerate(rules):
        extra = set(rule.keys()) - allowed
        assert not extra, f"Rule {i} has unexpected keys {extra}: {rule}"


def test_all_values_are_nonempty_strings():
    with GENERAL_RULES_PATH.open(encoding="utf-8") as f:
        rules = json.load(f)
    for i, rule in enumerate(rules):
        for key in ("type1", "type2", "result"):
            val = rule[key]
            assert isinstance(val, str) and val.strip(), (
                f"Rule {i} key '{key}' is not a non-empty string: {val!r}"
            )


def test_spot_check_flame_swordsman():
    with GENERAL_RULES_PATH.open(encoding="utf-8") as f:
        rules = json.load(f)
    assert {
        "type1": "Fire (Mars)",
        "type2": "Warrior",
        "result": "Flame Swordsman",
    } in rules


def test_spot_check_koumori_dragon():
    with GENERAL_RULES_PATH.open(encoding="utf-8") as f:
        rules = json.load(f)
    assert {"type1": "Dragon", "type2": "Fiend", "result": "Koumori Dragon"} in rules


def test_spot_check_turtle_spellcaster():
    with GENERAL_RULES_PATH.open(encoding="utf-8") as f:
        rules = json.load(f)
    assert {
        "type1": "Turtle",
        "type2": "Spellcaster",
        "result": "30,000-Year White Turtle",
    } in rules


def test_spot_check_dark_elf_fiend_magic_moon():
    with GENERAL_RULES_PATH.open(encoding="utf-8") as f:
        rules = json.load(f)
    assert {
        "type1": "Elf",
        "type2": "Fiend Magic (Moon)",
        "result": "Dark Elf",
    } in rules


def test_no_duplicate_entries():
    with GENERAL_RULES_PATH.open(encoding="utf-8") as f:
        rules = json.load(f)
    triples = [(r["type1"], r["type2"], r["result"]) for r in rules]
    assert len(triples) == len(set(triples)), (
        "Duplicate (type1, type2, result) triples found"
    )
