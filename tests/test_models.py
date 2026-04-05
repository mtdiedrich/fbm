from fbm.models import Card, GeneralRule, ExactRule


def test_card_instantiation():
    card = Card(
        name="Ice Water",
        atk=1150,
        def_=900,
        groups=["Aqua", "Female"],
        primary_type="Aqua",
        secondary_types=["Female"],
    )
    assert card.name == "Ice Water"
    assert card.atk == 1150
    assert card.def_ == 900
    assert card.groups == ["Aqua", "Female"]
    assert card.primary_type == "Aqua"
    assert card.secondary_types == ["Female"]


def test_card_default_secondary_types():
    card = Card(
        name="Battle Ox",
        atk=1700,
        def_=1000,
        groups=["Warrior"],
        primary_type="Beast-Warrior",
    )
    assert card.secondary_types == []


def test_card_secondary_types_not_shared():
    card_a = Card(name="A", atk=0, def_=0, groups=[], primary_type="Aqua")
    card_b = Card(name="B", atk=0, def_=0, groups=[], primary_type="Aqua")
    card_a.secondary_types.append("Female")
    assert card_b.secondary_types == []


def test_card_groups_not_shared():
    card_a = Card(name="A", atk=0, def_=0, groups=[], primary_type="Aqua")
    card_b = Card(name="B", atk=0, def_=0, groups=[], primary_type="Aqua")
    card_a.groups.append("Dragon")
    assert card_b.groups == []


def test_general_rule_instantiation():
    rule = GeneralRule(type1="Fire (Mars)", type2="Warrior", result="Flame Swordsman")
    assert rule.type1 == "Fire (Mars)"
    assert rule.type2 == "Warrior"
    assert rule.result == "Flame Swordsman"


def test_general_rule_importable():
    from fbm.models import GeneralRule  # noqa: F401


def test_exact_rule_instantiation():
    rule = ExactRule(card1="Battle Ox", card2="Dragon Statue", result="Baby Dragon")
    assert rule.card1 == "Battle Ox"
    assert rule.card2 == "Dragon Statue"
    assert rule.result == "Baby Dragon"


def test_models_importable_from_fbm_models():
    from fbm.models import Card, GeneralRule, ExactRule  # noqa: F401
