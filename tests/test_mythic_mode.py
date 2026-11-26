from src.metatron.mythic_mode import MythicModeEngine, SafetyAssessment, UserPreferences


def test_high_risk_is_only_reported_as_caller_supplied():
    engine = MythicModeEngine(UserPreferences(modes={"NATURE": True}))
    result = engine.generate_location_narrative(
        "Sample Park", {"time_of_day": "day", "weather": "clear"},
        SafetyAssessment("HIGH"),
    )
    assert "CALLER-SUPPLIED HIGH RISK LABEL" in result
    assert "cannot verify" in result
    assert engine.metrics["caller_flagged_safety_labels"] == 1


def test_critical_label_does_not_claim_the_module_detected_danger():
    engine = MythicModeEngine()
    result = engine.generate_location_narrative(
        "Sample Place", {}, SafetyAssessment("CRITICAL")
    )
    assert "CALLER-SUPPLIED CRITICAL RISK LABEL" in result
    assert "cannot detect or verify an emergency" in result
    assert "Immediate danger detected" not in result


def test_disabled_engine_returns_no_story():
    engine = MythicModeEngine(UserPreferences(enabled=False))
    assert engine.generate_location_narrative(
        "Sample Place", {}, SafetyAssessment("LOW")
    ) == "Mythic Mode is currently disabled."


def test_invalid_risk_label_is_rejected():
    try:
        SafetyAssessment("UNKNOWN")
    except ValueError:
        return
    raise AssertionError("Expected invalid risk label to raise ValueError")


def test_intensity_is_clamped_and_is_reserved():
    prefs = UserPreferences(intensity=99)
    assert prefs.intensity == 5
