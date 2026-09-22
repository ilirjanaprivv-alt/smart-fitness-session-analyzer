from data_generator import generate_fitness_data
from models import Participant, Observation, Session
from analysis import classify_session

def create_session(scenario):
    profile, observations = generate_fitness_data(
        participant_id="P001",
        scenario=scenario,
        seed=42,
        number_of_windows=10
    )

    participant = Participant(
        profile.get("participant_id"),
        profile.get("baseline_heart_rate"),
        profile.get("baseline_skin_response"),
        profile.get("baseline_temperature")
    )

    valid_observations = []

    for observation in observations:
        observation_object = Observation(
            observation.get("timestamp"),
            observation.get("heart_rate"),
            observation.get("skin_response"),
            observation.get("temperature"),
            observation.get("activity_level"),
            observation.get("signal_quality")
        )

        if observation_object.is_valid():
            valid_observations.append(observation_object)

    return Session(participant, valid_observations)

def test_resting():
    session = create_session("resting")
    result = classify_session(session)

    assert result == "resting"

def test_moderate_activity():
    session = create_session("moderate_activity")
    result = classify_session(session)

    assert result == "moderate activity"

def test_high_activity():
    session = create_session("high_activity")
    result = classify_session(session)

    assert result == "high activity"

def test_recovery():
    session = create_session("recovery")
    result = classify_session(session)

    assert result == "recovering"

def test_poor_quality():
    session = create_session("poor_quality")
    result = classify_session(session)

    assert result == "insufficient data"

def run_tests():
    test_resting()
    print("Resting test passed.")

    test_moderate_activity()
    print("Moderate activity test passed.")

    test_high_activity()
    print("High activity test passed.")

    test_recovery()
    print("Recovery test passed.")

    test_poor_quality()
    print("Poor quality test passed.")

    print("\nAll tests passed successfully.")


if __name__ == "__main__":
    run_tests()