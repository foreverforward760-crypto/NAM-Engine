# src/metatron/mythic_mode.py
"""
METATRON MYTHIC MODE — narrative-template prototype.

This module selects a narrative style at random and inserts location/context
strings into fixed templates. It does not retrieve historical or geographic
facts, monitor a location, calculate safety risk, or verify caller-supplied
risk labels.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional
import random


RiskLabel = Literal["LOW", "MODERATE", "HIGH", "CRITICAL"]


@dataclass
class UserPreferences:
    enabled: bool = True
    modes: Dict[str, bool] = field(default_factory=lambda: {
        "HISTORICAL": True,
        "NATURE": True,
        "CULTURAL": True,
        "GEOGRAPHIC": True,
        "HEROIC": False,
        "SPOOKY": False,
    })
    # Reserved preference; current narrative templates do not use intensity.
    intensity: int = 3

    def __post_init__(self) -> None:
        self.intensity = max(1, min(5, int(self.intensity)))


@dataclass
class SafetyAssessment:
    """
    A risk label supplied by the caller, not computed by this module.

    The engine does not independently assess, sense, or verify location safety.
    """
    risk: RiskLabel
    details: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized = str(self.risk).upper()
        if normalized not in {"LOW", "MODERATE", "HIGH", "CRITICAL"}:
            raise ValueError("risk must be LOW, MODERATE, HIGH, or CRITICAL")
        self.risk = normalized  # type: ignore[assignment]


class MythicModeEngine:
    """
    Small narrative-template skeleton.

    Mode selection is random. Safety wording is based solely on the
    SafetyAssessment label provided by the caller. No external services,
    live location feeds, emergency dispatch, or risk-detection logic exist.
    """

    def __init__(self, user_prefs: Optional[UserPreferences] = None):
        self.user_prefs = user_prefs or UserPreferences()
        self.metrics: Dict[str, Any] = {
            "stories_played": 0,
            # Counts caller-supplied HIGH/CRITICAL labels, not detected events.
            "caller_flagged_safety_labels": 0,
        }

    def generate_location_narrative(
        self,
        location_name: str,
        context: Dict[str, Any],
        safety: SafetyAssessment,
    ) -> str:
        """Return a templated narrative for a location and supplied context."""
        if not self.user_prefs.enabled:
            return "Mythic Mode is currently disabled."

        mode = self._select_mode()
        base_story = self._generate_base_story(mode, location_name, context)
        story_with_safety = self._integrate_safety(base_story, safety)

        self.metrics["stories_played"] += 1
        return story_with_safety

    def _select_mode(self) -> str:
        enabled_modes = [mode for mode, on in self.user_prefs.modes.items() if on]
        return random.choice(enabled_modes) if enabled_modes else "HISTORICAL"

    def _generate_base_story(
        self, mode: str, location_name: str, context: Dict[str, Any]
    ) -> str:
        tod = context.get("time_of_day", "day")
        weather = context.get("weather", "clear")

        if mode == "HISTORICAL":
            return (
                f"You’re walking through {location_name}, a place layered with history. "
                f"Under the {weather} {tod}, the streets carry echoes of everyone who "
                f"passed here before you."
            )
        if mode == "NATURE":
            return (
                f"Here in {location_name}, the living world is working quietly in the background. "
                f"Even in this {weather} {tod}, roots, leaves, and tiny lives are busy."
            )
        if mode == "CULTURAL":
            return (
                f"{location_name} is more than buildings—it’s a story of people, migrations, "
                f"languages and traditions woven together over time."
            )
        if mode == "GEOGRAPHIC":
            return (
                f"The shape of {location_name} was carved long before you arrived—by rivers, "
                f"glaciers, fault lines, and human decisions stacked on top."
            )
        if mode == "HEROIC":
            return (
                f"Today, {location_name} is the next chapter of your quest. "
                f"You’re the main character here—moving through a map that invites curiosity."
            )
        if mode == "SPOOKY":
            return (
                f"Locals whisper that {location_name} keeps its own memories. "
                f"On nights like this, people say the past feels just a little closer."
            )

        return f"You are in {location_name}."

    def _integrate_safety(self, story: str, safety: SafetyAssessment) -> str:
        risk = safety.risk.upper()

        if risk == "LOW":
            return (
                story
                + " The caller supplied a LOW risk label. This module does not verify "
                "current area safety; remain aware of your surroundings."
            )

        if risk == "MODERATE":
            return (
                story
                + " The caller supplied a MODERATE risk label. This module cannot verify "
                "current conditions; consult reliable local information."
            )

        if risk == "HIGH":
            self.metrics["caller_flagged_safety_labels"] += 1
            return (
                "[CALLER-SUPPLIED HIGH RISK LABEL]\n"
                "This module cannot verify the rating or current conditions. Consider "
                "reliable local safety information and established travel precautions.\n\n"
                + story
            )

        if risk == "CRITICAL":
            self.metrics["caller_flagged_safety_labels"] += 1
            return (
                "[CALLER-SUPPLIED CRITICAL RISK LABEL]\n"
                "This module cannot detect or verify an emergency. If you believe you are "
                "in immediate danger, move to safety and contact local emergency services."
            )

        return story
