"""
Shared pytest fixtures for test setup and teardown.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Arrange: Provide a TestClient for making HTTP requests to the app.
    """
    return TestClient(app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """
    Arrange: Reset the activities dictionary before each test to prevent
    cross-test contamination. Uses monkeypatch to inject fresh data.
    """
    fresh_data = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    monkeypatch.setattr("src.app.activities", fresh_data)
    return fresh_data
