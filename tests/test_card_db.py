from pathlib import Path

from fbm.card_db import CardDB
from fbm.models import Card

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "cards_fixture.json"


def test_load_returns_carddb():
    db = CardDB.load(FIXTURE_PATH)
    assert isinstance(db, CardDB)


def test_len_matches_fixture():
    db = CardDB.load(FIXTURE_PATH)
    assert len(db) == 10


def test_get_known_card():
    db = CardDB.load(FIXTURE_PATH)
    card = db.get("Ice Water")
    assert card is not None
    assert card.atk == 1150
    assert card.def_ == 900


def test_get_returns_card_instance():
    db = CardDB.load(FIXTURE_PATH)
    card = db.get("Celtic Guardian")
    assert isinstance(card, Card)


def test_get_unknown_card():
    db = CardDB.load(FIXTURE_PATH)
    assert db.get("No Such Card") is None


def test_get_case_insensitive():
    db = CardDB.load(FIXTURE_PATH)
    assert db.get("ice water") == db.get("Ice Water")
    assert db.get("ICE WATER") == db.get("Ice Water")


def test_get_secondary_types():
    db = CardDB.load(FIXTURE_PATH)
    card = db.get("Dark Witch")
    assert card is not None
    assert "Female" in card.secondary_types
    assert "AngelWinged" in card.secondary_types


def test_search_partial_match():
    db = CardDB.load(FIXTURE_PATH)
    results = db.search("water")
    names = [c.name for c in results]
    assert "Ice Water" in names


def test_search_no_match():
    db = CardDB.load(FIXTURE_PATH)
    assert db.search("xyznonexistent") == []


def test_search_case_insensitive():
    db = CardDB.load(FIXTURE_PATH)
    lower = db.search("ice water")
    upper = db.search("ICE WATER")
    assert lower == upper
    assert len(lower) > 0


def test_load_default_path():
    db = CardDB.load()
    assert isinstance(db, CardDB)
