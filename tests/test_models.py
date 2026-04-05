from fbm.models import Card, GeneralRule, GeneralRuleResult, ExactRule


def test_card_instantiation():
    card = Card(
        name="Ice Water",
        atk=1150,
        def_=900,
        g1="Npt",
        g2="Mon",
        primary_type="Aqua",
        secondary_types=["Bugrothian", "Female"],
    )
    assert card.name == "Ice Water"
    assert card.atk == 1150
    assert card.def_ == 900
    assert card.g1 == "Npt"
    assert card.g2 == "Mon"
    assert card.primary_type == "Aqua"
    assert card.secondary_types == ["Bugrothian", "Female"]


def test_card_default_secondary_types():
    card = Card(
        name="Battle Ox",
        atk=1700,
        def_=1000,
        g1="Mrs",
        g2="Sun",
        primary_type="Beast-Warrior",
    )
    assert card.secondary_types == []


def test_card_secondary_types_not_shared():
    card_a = Card(name="A", atk=0, def_=0, g1="NUL", g2="NUL", primary_type="Aqua")
    card_b = Card(name="B", atk=0, def_=0, g1="NUL", g2="NUL", primary_type="Aqua")
    card_a.secondary_types.append("Female")
    assert card_b.secondary_types == []


def test_general_rule_result_instantiation():
    grr = GeneralRuleResult(
        name="Ice Water",
        atk_threshold=1150,
        conflicts=["Wow Warrior", "Tatsunootoshigo"],
    )
    assert grr.name == "Ice Water"
    assert grr.atk_threshold == 1150
    assert grr.conflicts == ["Wow Warrior", "Tatsunootoshigo"]


def test_general_rule_result_default_conflicts():
    grr = GeneralRuleResult(name="Enchanting Mermaid", atk_threshold=1200)
    assert grr.conflicts == []


def test_general_rule_instantiation():
    rule = GeneralRule(
        type1="Female",
        type2="Fish",
        tiers=[
            GeneralRuleResult("Ice Water", 1150, ["Wow Warrior", "Tatsunootoshigo"]),
            GeneralRuleResult("Enchanting Mermaid", 1200, []),
            GeneralRuleResult(
                "Amazon of the Seas",
                1300,
                [
                    "Wow Warrior",
                    "Tatsunootoshigo",
                    "Dark Witch",
                    "Queen of Autumn Leaves",
                ],
            ),
        ],
    )
    assert rule.type1 == "Female"
    assert rule.type2 == "Fish"
    assert len(rule.tiers) == 3
    assert rule.tiers[0].name == "Ice Water"
    assert rule.tiers[2].atk_threshold == 1300


def test_general_rule_default_tiers():
    rule = GeneralRule(type1="Aqua", type2="Thunder")
    assert rule.tiers == []


def test_exact_rule_instantiation():
    rule = ExactRule(card1="Battle Ox", card2="Dragon Statue", result="Baby Dragon")
    assert rule.card1 == "Battle Ox"
    assert rule.card2 == "Dragon Statue"
    assert rule.result == "Baby Dragon"


def test_models_importable_from_fbm_models():
    from fbm.models import Card, GeneralRuleResult, GeneralRule, ExactRule  # noqa: F401
