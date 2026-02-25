from __future__ import annotations

import csv
from io import StringIO

from sqlalchemy.orm import Session

from app.core.models import PropertyListing


def import_csv(db: Session, content: str) -> int:
    reader = csv.DictReader(StringIO(content))
    count = 0
    for row in reader:
        db.add(
            PropertyListing(
                agent_id=int(row["agent_id"]),
                title=row["title"],
                suburb=row["suburb"],
                city=row["city"],
                province=row["province"],
                price=float(row["price"]),
                beds=int(row["beds"]),
                baths=int(row["baths"]),
                parking=int(row["parking"]),
                features_json=row["features_json"].split("|"),
                status=row["status"],
            )
        )
        count += 1
    db.commit()
    return count
