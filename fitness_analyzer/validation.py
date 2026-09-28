import re
from fitness_analyzer.exceptions import InvalidIdentifierError

from fitness_analyzer.exceptions import (InvalidIdentifierError, InvalidRecordError)

def validate_participant_id(participant_id):
    pattern = r"P\d{3}"
    match = re.fullmatch(pattern, participant_id)

    if match is None:
        raise InvalidIdentifierError(
            f"Invalid participant ID: {participant_id}"
        )

    return True


def validate_session_id(session_id):
    pattern = r"FIT-\d{4}-\d{3}"
    match = re.fullmatch(pattern, session_id)

    if match is None:
        raise InvalidIdentifierError(
            f"Invalid session ID: {session_id}"
        )

    return True


def validate_measurement(field, value):
    if field == "timestamp" and value < 0:
        raise InvalidRecordError(
            "Timestamp must be 0 or greater."
        )

    elif field == "heart_rate" and (value < 35 or value > 205):
        raise InvalidRecordError(
            "Heart rate must be between 35 and 205."
        )

    elif field == "skin_response" and value < 0:
        raise InvalidRecordError(
            "Skin response must be 0 or greater."
        )

    elif field == "temperature" and (value < 25 or value > 42):
        raise InvalidRecordError(
            "Temperature must be between 25 and 42."
        )

    elif field == "activity_level" and (value < 0 or value > 1):
        raise InvalidRecordError(
            "Activity level must be between 0 and 1."
        )

    elif field == "signal_quality" and (value < 0.60 or value > 1):
        raise InvalidRecordError(
            "Signal quality must be between 0.60 and 1."
        )