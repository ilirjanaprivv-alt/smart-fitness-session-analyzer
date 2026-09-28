import csv

from fitness_analyzer.models import Participant, Observation, Session
from fitness_analyzer.validation import (validate_participant_id, validate_session_id, validate_measurement)
from fitness_analyzer.exceptions import (InvalidIdentifierError, InvalidRecordError)


def load_participants(filename):
    participants = {}
    rejected_records = []

    required_fields = [
        "participant_id",
        "name",
        "baseline_heart_rate",
        "baseline_skin_response",
        "baseline_temperature"
    ]

    try:
        with open(filename, encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row_number, row in enumerate(reader, start=2):

                # Check for unexpected extra columns
                if None in row:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": "row",
                        "reason": "Unexpected number of columns"
                    })
                    continue

                # Check for missing fields or values
                missing_field = None

                for field in required_fields:
                    if (
                        field not in row
                        or row[field] is None
                        or row[field].strip() == ""
                    ):
                        missing_field = field
                        break

                if missing_field is not None:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": missing_field,
                        "reason": "Missing required value"
                    })
                    continue

                participant_id = row["participant_id"]
                name = row["name"]

                # Validate participant ID
                try:
                    validate_participant_id(participant_id)

                except InvalidIdentifierError as error:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": "participant_id",
                        "reason": str(error)
                    })
                    continue

                # Convert baseline heart rate
                try:
                    baseline_heart_rate = int(
                        row["baseline_heart_rate"]
                    )

                except ValueError:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": "baseline_heart_rate",
                        "reason": (
                            "Invalid numeric value: "
                            f"{row['baseline_heart_rate']}"
                        )
                    })
                    continue

                # Convert baseline skin response
                try:
                    baseline_skin_response = float(
                        row["baseline_skin_response"]
                    )

                except ValueError:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": "baseline_skin_response",
                        "reason": (
                            "Invalid numeric value: "
                            f"{row['baseline_skin_response']}"
                        )
                    })
                    continue

                # Convert baseline temperature
                try:
                    baseline_temperature = float(
                        row["baseline_temperature"]
                    )

                except ValueError:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": "baseline_temperature",
                        "reason": (
                            "Invalid numeric value: "
                            f"{row['baseline_temperature']}"
                        )
                    })
                    continue

                # Create Participant object
                try:
                    participant = Participant(
                        participant_id,
                        name,
                        baseline_heart_rate,
                        baseline_skin_response,
                        baseline_temperature
                    )

                except ValueError as error:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": "baseline_heart_rate",
                        "reason": str(error)
                    })
                    continue

                participants[participant_id] = participant

    except FileNotFoundError:
        print(f"File not found: {filename}")

    except PermissionError:
        print(f"Permission denied: {filename}")

    except csv.Error as error:
        print(f"CSV error in {filename}: {error}")

    return participants, rejected_records

def load_sessions(filename, participants):
    sessions = {}
    rejected_records = []
    session_row_counts = {}

    required_fields = [
        "session_id",
        "participant_id",
        "timestamp",
        "heart_rate",
        "skin_response",
        "temperature",
        "activity_level",
        "signal_quality"
    ]

    numeric_fields = {
        "timestamp": int,
        "heart_rate": float,
        "skin_response": float,
        "temperature": float,
        "activity_level": float,
        "signal_quality": float
    }

    try:
        with open(filename, encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row_number, row in enumerate(reader, start=2):

                raw_session_id = row.get("session_id")

                if (
                    raw_session_id is not None
                    and raw_session_id.strip() != ""
                ):
                    if raw_session_id not in session_row_counts:
                        session_row_counts[raw_session_id] = 0

                    session_row_counts[raw_session_id] += 1

                # 1. Check for unexpected extra columns
                if None in row:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": "row",
                        "reason": "Unexpected number of columns"
                    })
                    continue

                # 2. Check for missing fields or values
                missing_field = None

                for field in required_fields:
                    if (
                        field not in row
                        or row[field] is None
                        or row[field].strip() == ""
                    ):
                        missing_field = field
                        break

                if missing_field is not None:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": missing_field,
                        "reason": "Missing required value"
                    })
                    continue

                session_id = row["session_id"]
                participant_id = row["participant_id"]

                # 3. Validate session ID
                try:
                    validate_session_id(session_id)

                except InvalidIdentifierError as error:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": "session_id",
                        "reason": str(error)
                    })
                    continue

                # 4. Validate participant ID
                try:
                    validate_participant_id(participant_id)

                except InvalidIdentifierError as error:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": "participant_id",
                        "reason": str(error)
                    })
                    continue

                # 5. Check that participant exists
                if participant_id not in participants:
                    rejected_records.append({
                        "filename": str(filename),
                        "row": row_number,
                        "field": "participant_id",
                        "reason": (
                            f"Unknown participant ID: "
                            f"{participant_id}"
                        )
                    })
                    continue

                participant = participants[participant_id]

                # 6. Convert numeric values
                converted_values = {}
                conversion_failed = False

                for field, converter in numeric_fields.items():
                    try:
                        converted_values[field] = converter(
                            row[field]
                        )

                    except ValueError:
                        rejected_records.append({
                            "filename": str(filename),
                            "row": row_number,
                            "field": field,
                            "reason": (
                                f"Invalid numeric value: "
                                f"{row[field]}"
                            )
                        })
                        conversion_failed = True
                        break

                    except KeyError:
                        rejected_records.append({
                            "filename": str(filename),
                            "row": row_number,
                            "field": field,
                            "reason": "Missing required field"
                        })
                        conversion_failed = True
                        break

                if conversion_failed:
                    continue

                # 7. Validate numeric ranges and signal quality
                measurement_failed = False

                for field, value in converted_values.items():
                    try:
                        validate_measurement(field, value)

                    except InvalidRecordError as error:
                        rejected_records.append({
                            "filename": str(filename),
                            "row": row_number,
                            "field": field,
                            "reason": str(error)
                        })
                        measurement_failed = True
                        break

                if measurement_failed:
                    continue

                # 8. Create Observation object
                observation = Observation(
                    converted_values["timestamp"],
                    converted_values["heart_rate"],
                    converted_values["skin_response"],
                    converted_values["temperature"],
                    converted_values["activity_level"],
                    converted_values["signal_quality"]
                )

                # 9. Create Session object
                if session_id not in sessions:
                    sessions[session_id] = Session(
                        session_id,
                        participant,
                        []
                    )

                # 10. Add observation to the correct session
                sessions[session_id].observations.append(
                    observation
                )

    except FileNotFoundError:
        print(f"File not found: {filename}")

    except PermissionError:
        print(f"Permission denied: {filename}")

    except csv.Error as error:
        print(f"CSV error in {filename}: {error}")

    return sessions, rejected_records, session_row_counts