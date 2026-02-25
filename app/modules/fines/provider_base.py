from __future__ import annotations

from typing import Protocol


class FineProviderBase(Protocol):
    def fetch_fines(self, id_number: str, plates: list[str]) -> list[dict[str, object]]: ...
