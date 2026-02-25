from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import PropertyAgent, PropertyLead, PropertyListing


def search_listings(db: Session, area: str, max_price: float, beds: int, features: list[str]) -> list[PropertyListing]:
    listings = db.scalars(
        select(PropertyListing).where(
            PropertyListing.status == "active",
            PropertyListing.price <= max_price,
            PropertyListing.beds >= beds,
        )
    ).all()
    listings = [l for l in listings if area.lower() in {l.suburb.lower(), l.city.lower()}]
    listings = [l for l in listings if all(feature in l.features_json for feature in features)]

    def rank(item: PropertyListing) -> tuple[int, float]:
        agent = db.get(PropertyAgent, item.agent_id)
        featured = 1 if agent and agent.plan == "featured" and item.suburb.lower() in [s.lower() for s in agent.suburb_focus_json] else 0
        return (featured, -float(item.price))

    return sorted(listings, key=rank, reverse=True)[:10]


def create_lead(db: Session, user_id: object, agent_id: int, listing_id: int | None, lead_type: str) -> PropertyLead:
    lead = PropertyLead(user_id=user_id, agent_id=agent_id, listing_id=listing_id, lead_type=lead_type, status="sent")
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
