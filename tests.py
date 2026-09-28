from pathlib import Path

from fitness_analyzer.csv_reader import (load_participants, load_sessions)
from fitness_analyzer.analysis import FitnessAnalyzer
from fitness_analyzer.validation import (validate_participant_id, validate_session_id, validate_measurement)
from fitness_analyzer.exceptions import (InvalidIdentifierError, InvalidRecordError)


DATA_DIR = Path("data")

PARTICIPANTS_FILE = DATA_DIR / "participants.csv"
VALID_SESSIONS_FILE = DATA_DIR / "fitness_sessions.csv"
INVALID_SESSIONS_FILE = DATA_DIR / "fitness_sessions_invalid.csv"


def assert_raises(exception_type, function, *args):
    try:
        function(*args)

    except exception_type:
        return

    assert False, (
        f"Expected {exception_type.__name__} "
        f"to be raised."
    )


def test_valid_case():
    participants = load_participants(
        PARTICIPANTS_FILE
    )

    assert len(participants) > 0
    assert "P001" in participants

    sessions, rejected_records, session_row_counts = load_sessions(
        VALID_SESSIONS_FILE,
        participants
    )

    assert len(sessions) > 0
    assert len(session_row_counts) > 0

    for session in sessions.values():
        assert len(session.observations) > 0

        classification = FitnessAnalyzer.classify_session(
            session
        )

        assert classification in [
            "resting",
            "moderate activity",
            "high activity",
            "recovering",
            "insufficient data"
        ]


def test_classifications():
    participants = load_participants(
        PARTICIPANTS_FILE
    )

    sessions, rejected_records, session_row_counts = load_sessions(
        VALID_SESSIONS_FILE,
        participants
    )

    assert FitnessAnalyzer.classify_session(
        sessions["FIT-2026-001"]
    ) == "resting"

    assert FitnessAnalyzer.classify_session(
        sessions["FIT-2026-002"]
    ) == "moderate activity"

    assert FitnessAnalyzer.classify_session(
        sessions["FIT-2026-003"]
    ) == "high activity"

    assert FitnessAnalyzer.classify_session(
        sessions["FIT-2026-004"]
    ) == "recovering"


def test_invalid_case():
    participants = load_participants(
        PARTICIPANTS_FILE
    )

    sessions, rejected_records, session_row_counts = load_sessions(
        INVALID_SESSIONS_FILE,
        participants
    )

    assert len(rejected_records) > 0
    assert len(session_row_counts) > 0

    for record in rejected_records:
        assert "filename" in record
        assert "row" in record
        assert "field" in record
        assert "reason" in record

        assert record["filename"] != ""
        assert record["row"] >= 2
        assert record["field"] != ""
        assert record["reason"] != ""


def test_missing_file_case():
    participants = load_participants(
        PARTICIPANTS_FILE
    )

    missing_file = DATA_DIR / "does_not_exist.csv"

    sessions, rejected_records, session_row_counts = load_sessions(
        missing_file,
        participants
    )

    assert sessions == {}
    assert rejected_records == []
    assert session_row_counts == {}


def test_boundary_case():
    # Lowest and highest accepted values
    validate_measurement(
        "timestamp",
        0
    )

    validate_measurement(
        "heart_rate",
        35
    )

    validate_measurement(
        "heart_rate",
        205
    )

    validate_measurement(
        "skin_response",
        0
    )

    validate_measurement(
        "temperature",
        25
    )

    validate_measurement(
        "temperature",
        42
    )

    validate_measurement(
        "activity_level",
        0
    )

    validate_measurement(
        "activity_level",
        1
    )

    validate_measurement(
        "signal_quality",
        0.60
    )

    validate_measurement(
        "signal_quality",
        1
    )

    # Values just outside accepted boundaries
    assert_raises(
        InvalidRecordError,
        validate_measurement,
        "timestamp",
        -1
    )

    assert_raises(
        InvalidRecordError,
        validate_measurement,
        "heart_rate",
        34
    )

    assert_raises(
        InvalidRecordError,
        validate_measurement,
        "heart_rate",
        206
    )

    assert_raises(
        InvalidRecordError,
        validate_measurement,
        "skin_response",
        -0.1
    )

    assert_raises(
        InvalidRecordError,
        validate_measurement,
        "temperature",
        24.9
    )

    assert_raises(
        InvalidRecordError,
        validate_measurement,
        "temperature",
        42.1
    )

    assert_raises(
        InvalidRecordError,
        validate_measurement,
        "activity_level",
        -0.1
    )

    assert_raises(
        InvalidRecordError,
        validate_measurement,
        "activity_level",
        1.1
    )

    assert_raises(
        InvalidRecordError,
        validate_measurement,
        "signal_quality",
        0.59
    )

    assert_raises(
        InvalidRecordError,
        validate_measurement,
        "signal_quality",
        1.01
    )


def test_identifier_validation():
    assert validate_participant_id(
        "P001"
    ) is True

    assert validate_session_id(
        "FIT-2026-001"
    ) is True

    assert_raises(
        InvalidIdentifierError,
        validate_participant_id,
        "P01"
    )

    assert_raises(
        InvalidIdentifierError,
        validate_participant_id,
        "ABC"
    )

    assert_raises(
        InvalidIdentifierError,
        validate_participant_id,
        "P0001"
    )

    assert_raises(
        InvalidIdentifierError,
        validate_session_id,
        "FIT-26-001"
    )

    assert_raises(
        InvalidIdentifierError,
        validate_session_id,
        "FIT-2026-01"
    )

    assert_raises(
        InvalidIdentifierError,
        validate_session_id,
        "ABC-2026-001"
    )


def run_tests():
    test_valid_case()
    print("Valid case test passed.")

    test_classifications()
    print("Classification tests passed.")

    test_invalid_case()
    print("Invalid case test passed.")

    test_missing_file_case()
    print("Missing-file test passed.")

    test_boundary_case()
    print("Boundary tests passed.")

    test_identifier_validation()
    print("Identifier validation tests passed.")

    print("\nAll Assignment II tests passed successfully.")


if __name__ == "__main__":
    run_tests()