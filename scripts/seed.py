from __future__ import annotations

from app.core.db import SessionLocal
from app.core.models import PropertyAgent, PropertyListing, SafetyContact, User


def main() -> None:
    db = SessionLocal()
    user = User(phone="27820000000")
    db.add(user)
    db.flush()
    agent = PropertyAgent(
        agency_name="PingSA Realty",
        agent_name="Nomsa",
        phone="27821234567",
        email="nomsa@example.com",
        suburb_focus_json=["Rondebosch"],
        plan="featured",
        billing_status="active",
    )
    db.add(agent)
    db.flush()
    db.add(PropertyListing(agent_id=agent.id, title="2 Bed Garden Flat", suburb="Rondebosch", city="Cape Town", province="WC", price=1850000, beds=2, baths=1, parking=1, features_json=["garden", "pet_friendly"], status="active"))
    db.add(SafetyContact(user_id=user.id, name="Mom", phone="27829876543", priority=1))
    db.commit()


if __name__ == "__main__":
    main()
