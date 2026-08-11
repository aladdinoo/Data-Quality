from rules.loader import RuleLoader


EXPECTED_RULES = {
    "email_validation",
    "phone_validation",
    "website_validation",
    "zip_validation",
    "name_validation",
    "date_validation",
    "duplicate_validation",
    "schema_validation",
    "invariant_validation",
    "pii_validation",
}


def test_rule_loader_loads_all_expected_rules():
    registry = RuleLoader().load()

    loaded_names = {
        rule.name
        for rule in registry
    }

    assert loaded_names == EXPECTED_RULES


def test_rule_loader_loads_exactly_ten_rules():
    registry = RuleLoader().load()

    assert len(registry) == 10


def test_loaded_rules_have_metadata():
    registry = RuleLoader().load()

    for rule in registry:
        assert rule.metadata is not None
        assert rule.name
        assert rule.version
        assert rule.metadata.identifier


def test_loaded_rules_are_enabled():
    registry = RuleLoader().load()

    for rule in registry:
        assert rule.metadata.enabled is True


def test_loaded_rules_are_base_rules():
    from rules.base import BaseRule

    registry = RuleLoader().load()

    for rule in registry:
        assert isinstance(rule, BaseRule)