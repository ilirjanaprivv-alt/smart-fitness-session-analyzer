import re
from fitness_analyzer.exceptions import InvalidIdentifierError

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