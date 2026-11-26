# NAM Engine — Narrative Prototype and Concept Documents

## Repository contents

This repository contains:
- NAM concept and architecture documents in PDF format.
- src/metatron/mythic_mode.py, a small Python narrative-template prototype.
- Regression tests for the prototype.

## What the code actually does

The Mythic Mode module:
- Randomly selects one enabled narrative style.
- Inserts a supplied location name and context strings into fixed text templates.
- Appends a safety notice based only on a risk label supplied by the caller.

It does not:
- Access live maps, weather, crime, emergency, or location-safety feeds.
- Detect or calculate risk.
- Verify a caller-supplied LOW, MODERATE, HIGH, or CRITICAL label.
- Contact emergency services or provide navigation.
- Generate narratives with an external AI model.
- Use the intensity preference in the current templates.

The metric caller_flagged_safety_labels counts caller-supplied HIGH/CRITICAL labels; it is not a count of detected safety events. The module should not be described as a location-safety engine or a safety-monitoring system.

## Conceptual provenance

The project owner states that the underlying NAM concepts and product direction originated with him. AI systems generated the code and suggested technical mechanisms used to implement the concept. This is the owner's account, not a legal determination of copyright ownership or inventorship.

## Documentation status

The PDF documents are conceptual materials. Their full technical and factual contents have not been independently audited as part of this code review. Any scientific, historical, safety, or predictive claims require source verification and independent evaluation.

## License note

A repository-level MIT license is present. Its wording refers to software and associated documentation files. The owner should decide whether that license was intended to cover all PDFs and written materials in this repository before commercial licensing or transfer. The license has not been changed.

## Tests

```bash
python -m pip install pytest
pytest tests -q
```

Passing tests verify selected template and caller-supplied-label behavior only. They do not validate real-world safety, location risk, or the conceptual model.