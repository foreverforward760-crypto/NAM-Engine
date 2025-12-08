# src/metatron/mythic_mode.py

"""
METATRON MYTHIC MODE
Narrative-driven safety & discovery engine (skeleton implementation).
"""

from dataclasses import dataclass
from typing import Dict, Any, List
import random


@dataclass
class UserPreferences:
    enabled: bool = True
    modes: Dict[str, bool] = None
    intensity: int = 3  # 1–5

    def __post_init__(self):
        if self.modes is None:
            self.modes = {
                "HISTORICAL": True,
                "NATURE": True,
                "CULTURAL": True,
                "GEOGRAPHIC": True,
                "HEROIC": False,
                "SPOOKY": False,
            }


@dataclass
class SafetyAssessment:
    risk: str  # "LOW", "MODERATE", "HIGH", "CRITICAL"
    details: Dict[str, Any]


class MythicModeEngine:
    """
    High-level skeleton of the Mythic Mode engine.
    Does NOT depend on any external services yet.
    """

    def __init__(self, user_prefs: UserPreferences | None = None):
        self.user_prefs = user_prefs or UserPreferences()
        self.metrics: Dict[str, Any] = {
            "stories_played": 0,
            "safety_interrupts": 0,
        }

    # ---- Public API ----------------------------------------------------- #

    def generate_location_narrative(
        self,
        location_name: str,
        context: Dict[str, Any],
        safety: SafetyAssessment,
    ) -> str:
        """
        Main entry point: returns a single narrative string for a location.
        """
        if not self.user_prefs.enabled:
            return "Mythic Mode is currently disabled."

        mode = self._select_mode()
        base_story = self._generate_base_story(mode, location_name, context)
        story_with_safety = self._integrate_safety(base_story, safety)

        self.metrics["stories_played"] += 1
        return story_with_safety

    # ---- Internals ------------------------------------------------------ #

    def _select_mode(self) -> str:
        enabled_modes = [m for m, on in self.user_prefs.modes.items() if on]
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
                f"You’re the main character here—moving through a map that’s watching out for you."
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
            return story + " This area is generally considered low risk—stay aware, but enjoy your walk."

        if risk == "MODERATE":
            return (
                story
                + " Heads up: this area has some moderate risk. Stick to main paths, "
                "stay aware of your surroundings, and trust your instincts."
            )

        if risk == "HIGH":
            self.metrics["safety_interrupts"] += 1
            return (
                "[SAFETY PRIORITY]\n"
                "This area has a high risk rating. Stay in well-lit, populated spaces, "
                "avoid shortcuts, and consider changing routes.\n\n"
                + story
            )

        if risk == "CRITICAL":
            self.metrics["safety_interrupts"] += 1
            return (
                "[EMERGENCY]\n"
                "Immediate danger detected. Do not continue forward. Turn back, move toward a busy, well-lit area, "
                "and contact help if needed."
            )

        return story

