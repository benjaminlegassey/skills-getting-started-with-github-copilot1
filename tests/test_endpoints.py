"""
Integration tests for FastAPI endpoints using AAA pattern (Arrange-Act-Assert).
Tests the complete request/response flow for all API routes.
"""

import pytest


def test_get_root_redirects_to_index_html(client):
    """
    Test that GET / redirects to /static/index.html

    Arrange: TestClient is ready (via fixture)
    Act: Make GET request to /
    Assert: Verify redirect response
    """
    # Arrange
    # (setup via client fixture)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307  # Temporary redirect


def test_get_activities_returns_all_activities(client, fresh_activities):
    """
    Test that GET /activities returns all activities with correct structure.

    Arrange: Fresh activities data via fixture
    Act: Make GET request to /activities
    Assert: Verify response contains all activities and correct format
    """
    # Arrange
    # (setup via fresh_activities fixture)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    assert len(activities) == 3

    # Verify activity structure
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert len(chess_club["participants"]) == 2


def test_signup_success(client, fresh_activities):
    """
    Test successful signup for an activity.

    Arrange: Fresh activities data with Chess Club having 2 participants
    Act: Sign up a new participant
    Assert: Verify participant is added and response is correct
    """
    # Arrange
    new_email = "alice@mergington.edu"
    activity_name = "Chess Club"
    initial_count = len(fresh_activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "Signed up" in result["message"]
    assert new_email in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_count + 1


def test_signup_duplicate_email(client, fresh_activities):
    """
    Test that duplicate signups are rejected.

    Arrange: Fresh activities with existing participant "michael@mergington.edu"
    Act: Try to signup the same participant again
    Assert: Verify error response and participant count unchanged
    """
    # Arrange
    duplicate_email = "michael@mergington.edu"
    activity_name = "Chess Club"
    initial_count = len(fresh_activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": duplicate_email}
    )

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"].lower()
    assert len(fresh_activities[activity_name]["participants"]) == initial_count


def test_signup_nonexistent_activity(client, fresh_activities):
    """
    Test that signup to a nonexistent activity is rejected.

    Arrange: Fresh activities (does not include "Fake Activity")
    Act: Try to signup for nonexistent activity
    Assert: Verify 404 error response
    """
    # Arrange
    email = "test@mergington.edu"
    nonexistent_activity = "Fake Activity"

    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "not found" in result["detail"].lower()


def test_unregister_success(client, fresh_activities):
    """
    Test successful unregistration from an activity.

    Arrange: Fresh activities with existing participant
    Act: Delete/unregister the participant
    Assert: Verify participant is removed and response is correct
    """
    # Arrange
    email_to_remove = "michael@mergington.edu"
    activity_name = "Chess Club"
    initial_count = len(fresh_activities[activity_name]["participants"])
    assert email_to_remove in fresh_activities[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email_to_remove}
    )

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "Unregistered" in result["message"]
    assert email_to_remove not in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_count - 1


def test_unregister_not_registered(client, fresh_activities):
    """
    Test that unregistering a non-registered participant is rejected.

    Arrange: Fresh activities, email not registered for activity
    Act: Try to unregister someone not signed up
    Assert: Verify error response and participant list unchanged
    """
    # Arrange
    unregistered_email = "notregistered@mergington.edu"
    activity_name = "Chess Club"
    initial_count = len(fresh_activities[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": unregistered_email}
    )

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"].lower()
    assert len(fresh_activities[activity_name]["participants"]) == initial_count


def test_unregister_nonexistent_activity(client, fresh_activities):
    """
    Test that unregistering from a nonexistent activity is rejected.

    Arrange: Fresh activities (does not include "Fake Activity")
    Act: Try to unregister from nonexistent activity
    Assert: Verify 404 error response
    """
    # Arrange
    email = "test@mergington.edu"
    nonexistent_activity = "Fake Activity"

    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "not found" in result["detail"].lower()
