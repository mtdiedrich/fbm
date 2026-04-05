import json
from pathlib import Path

EXACT_RULES_PATH = (
    Path(__file__).parent.parent / "src" / "fbm" / "data" / "exact_rules.json"
)


def _load():
    with EXACT_RULES_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _pair_matches(rule: dict, c1: str, c2: str) -> bool:
    """Order-insensitive check: does this rule match the given pair?"""
    return (rule["card1"] == c1 and rule["card2"] == c2) or (
        rule["card1"] == c2 and rule["card2"] == c1
    )


def _find(rules, c1, c2, result):
    return any(_pair_matches(r, c1, c2) and r["result"] == result for r in rules)


def test_file_is_valid_json():
    rules = _load()
    assert isinstance(rules, list)


def test_total_rule_count():
    rules = _load()
    assert len(rules) == 150


def test_all_entries_have_required_keys():
    rules = _load()
    for rule in rules:
        assert "card1" in rule
        assert "card2" in rule
        assert "result" in rule


def test_spot_baby_dragon_battle_ox():
    rules = _load()
    assert _find(rules, "Battle Ox", "Dragon Statue", "Baby Dragon")


def test_spot_summoned_skull():
    rules = _load()
    assert _find(rules, "Time Wizard", "Embryonic Beast", "Summoned Skull")


def test_spot_gaia_dragon_champion():
    rules = _load()
    assert _find(
        rules, "Curse of Dragon", "Gaia the Fierce Knight", "Gaia the Dragon Champion"
    )


def test_spot_musician_king():
    rules = _load()
    assert _find(rules, "Celtic Guardian", "Sonic Maid", "Musician King")


def test_spot_red_eyes_b_skull_dragon():
    rules = _load()
    assert _find(rules, "Red-eyes B. Dragon", "Summoned Skull", "B. Skull Dragon")


def test_spot_harpie_sisters():
    rules = _load()
    assert _find(rules, "Elegant Egotist", "Harpie Lady", "Harpie Lady Sisters")


def test_spot_reaper_of_cards():
    rules = _load()
    assert _find(rules, "Koumori Dragon", "Saggi the Dark Clown", "Reaper of the Cards")


def test_spot_witty_phantom_armored():
    rules = _load()
    assert _find(rules, "Armored Zombie", "Wood Clown", "Witty Phantom")


def test_spot_dark_energy():
    rules = _load()
    assert _find(rules, "Yami", "Yami", "Dark Energy")


def test_no_duplicate_pairs():
    rules = _load()
    seen = set()
    for r in rules:
        key = (frozenset([r["card1"], r["card2"]]), r["result"])
        assert key not in seen, f"Duplicate rule: {r}"
        seen.add(key)
