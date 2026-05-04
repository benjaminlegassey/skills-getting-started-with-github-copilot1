"""
Unit tests for activity business logic using AAA pattern.
Tests isolated logic without HTTP layer.
"""

import pytest


def test_participant_duplicate_detection(fresh_activities):
    """
    Test that participant duplicate detection works correctly.

    Arrange: Get a Chess Club with existing participants
    Act: Check if a participant exists in the list
    Assert: Verify correct detection
    """
    # Arrange
    activity = fresh_activities["Chess Club"]
    existing_participant = "michael@mergington.edu"
    new_participant = "alice@mergington.edu"

    # Act & Assert
    assert existing_participant in activity["participants"]
    assert new_participant not in activity["participants"]


def test_participant_capacity_available(fresh_activities):
    """
    Test that we can calculate available spots in an activity.

    Arrange: Get activity with known capacity and participants
    Act: Calculate available spots
    Assert: Verify calculation is correct
    """
    # Arrange
    activity = fresh_activities["Chess Club"]
    max_capacity = activity["max_participants"]
    current_participants = len(activity["participants"])

    # Act
    available_spots = max_capacity - current_participants

    # Assert
    assert available_spots == 10  # 12 max - 2 participants
    assert available_spots > 0


def test_participant_list_modification(fresh_activities):
    """
    Test that participant list can be properly modified.

    Arrange: Get activity with participants
    Act: Add and remove a participant
    Assert: Verify modifications work correctly
    """
    # Arrange
    activity = fresh_activities["Programming Class"]
    new_email = "bob@mergington.edu"
    initial_count = len(activity["participants"])

    # Act - Add participant
    activity["participants"].append(new_email)

    # Assert - Added
    assert new_email in activity["participants"]
    assert len(activity["participants"]) == initial_count + 1

    # Act - Remove participant
    activity["participants"].remove(new_email)

    # Assert - Removed
    assert new_email not in activity["participants"]
    assert len(activity["participants"]) == initial_count


def test_activities_structure_integrity(fresh_activities):
    """
    Test that all activities have required fields.

    Arrange: Get all fresh activities
    Act: Check each activity for required structure
    Assert: Verify all fields are present and correct types
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]

    # Act & Assert
    for activity_name, activity_data in fresh_activities.items():
        for field in required_fields:
            assert field in activity_data, f"Missing '{field}' in {activity_name}"

        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)

        # All participants in list should be strings
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
