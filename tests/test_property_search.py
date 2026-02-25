from app.core.models import PropertyAgent, PropertyListing
from app.modules.property.service import search_listings


def test_property_featured_ranking(session) -> None:
    a1 = PropertyAgent(agency_name="A", agent_name="F", phone="1", email="a@a", suburb_focus_json=["Rondebosch"], plan="featured", billing_status="active")
    a2 = PropertyAgent(agency_name="B", agent_name="N", phone="2", email="b@b", suburb_focus_json=["Rondebosch"], plan="free", billing_status="active")
    session.add_all([a1, a2]); session.flush()
    session.add_all([
        PropertyListing(agent_id=a2.id, title="Normal", suburb="Rondebosch", city="Cape Town", province="WC", price=1000, beds=2, baths=1, parking=1, features_json=["garden"], status="active"),
        PropertyListing(agent_id=a1.id, title="Featured", suburb="Rondebosch", city="Cape Town", province="WC", price=1200, beds=2, baths=1, parking=1, features_json=["garden"], status="active"),
    ])
    session.commit()
    res = search_listings(session, "Rondebosch", 2000, 2, ["garden"])
    assert res[0].title == "Featured"
