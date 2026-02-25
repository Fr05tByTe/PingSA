from __future__ import annotations

from datetime import date


class MockFineProvider:
    def __init__(self, scenario: str = "baseline") -> None:
        self.scenario = scenario

    def fetch_fines(self, id_number: str, plates: list[str]) -> list[dict[str, object]]:
        seed = sum(ord(c) for c in id_number[-4:])
        out: list[dict[str, object]] = []
        for i, plate in enumerate(plates):
            out.append(
                {
                    "plate": plate,
                    "provider_reference": f"MOCK-{seed}-{i}",
                    "offence_summary": "Speeding",
                    "amount": 500.0,
                    "offence_date": date(2024, 1, 10),
                    "due_date": date(2024, 3, 10),
                    "status": "new",
                }
            )
        if self.scenario == "new_fine":
            out.append({"plate": plates[0], "provider_reference": "MOCK-NEW", "offence_summary": "Parking", "amount": 350.0, "offence_date": date(2024, 2, 2), "due_date": date(2024, 4, 2), "status": "new"})
        return out
