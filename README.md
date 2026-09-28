# Smart Fitness Session Analyzer

**Selected option:** Option A – Smart Fitness Session Analyzer  
**Student name:** Ilirijana Krasniqi  
**Student number:** 385512

## Project Description

This project is a file-based Python application that analyzes simulated wearable fitness-session data. It reads participant profiles and fitness-session records from CSV files, validates each record, groups observations by session, connects each session to an existing participant, performs the analysis from Assignment I, and writes summary and diagnostic output files.

The possible classifications are:

- `resting`
- `moderate activity`
- `high activity`
- `recovering`
- `insufficient data`

## Project Structure

```text
option_a_fitness/
├── data/
│   ├── participants.csv
│   ├── fitness_sessions.csv
│   └── fitness_sessions_invalid.csv
├── fitness_analyzer/
│   ├── __init__.py
│   ├── analysis.py
│   ├── csv_reader.py
│   ├── exceptions.py
│   ├── models.py
│   ├── reporting.py
│   └── validation.py
├── output/     # created by the program
│   ├── analysis_summary.csv
│   ├── analysis_report.txt
│   └── rejected_records.txt
├── main.py
├── tests.py
├── README.md
├── requirements.txt
└── .gitignore
```

The official CSV files in `data/` are used as input and are not modified by the program.

## Module Responsibilities

- `models.py` defines `Participant`, `Observation`, and `Session`.
- `validation.py` validates participant IDs, session IDs, numeric ranges, and signal quality.
- `exceptions.py` defines the custom exceptions `InvalidIdentifierError` and `InvalidRecordError`.
- `csv_reader.py` reads CSV files, converts values to suitable types, validates rows, records rejected session rows, groups observations by session ID, and connects sessions to participants.
- `analysis.py` calculates summaries, compares measurements with participant baselines, classifies sessions, and returns a structured dictionary for each session.
- `reporting.py` creates the output directory and writes the three required report files.
- `main.py` handles command-line arguments and coordinates the complete program flow.

## Object-Oriented Design

`Participant` stores a participant ID, name, and baseline values. The `baseline_heart_rate` value is controlled through a property, which demonstrates encapsulation.

`Observation` represents one sensor observation window.

`Session` demonstrates composition because one session contains one `Participant` object and a list of `Observation` objects.

`FitnessAnalyzer` contains static analysis methods because these operations do not require state from a separate analyzer object.

## Identifier Validation

Participant IDs must match:

```text
P followed by exactly three digits
Example: P001
```

Fitness session IDs must match:

```text
FIT-YYYY-NNN
Example: FIT-2026-001
```

The program uses `re.fullmatch()` for both identifier checks.

## Record Validation

Session rows are rejected when they contain missing required values, unexpected extra columns, values that cannot be converted to the required numeric type, invalid identifiers, unknown participant IDs, out-of-range measurements, or poor signal quality.

Accepted measurement ranges are:

- `timestamp >= 0`
- `35 <= heart_rate <= 205`
- `skin_response >= 0`
- `25 <= temperature <= 42`
- `0 <= activity_level <= 1`
- `0.60 <= signal_quality <= 1`

A signal-quality value below `0.60` is treated as a data-quality problem and the row is rejected.

For each rejected session row, the program records:

- source filename
- row number
- field
- reason

## Error Handling

The program uses the custom exceptions:

- `InvalidIdentifierError`
- `InvalidRecordError`

It also uses targeted handling for relevant built-in and CSV errors, including `FileNotFoundError`, `PermissionError`, `ValueError`, `KeyError`, and `csv.Error`.

## Analysis

For usable observations, the program calculates average, minimum, and maximum values for heart rate, skin response, temperature, activity level, and signal quality. It also compares heart rate, skin response, and temperature with the participant's personal baseline values.

Classification rules:

- `insufficient data`: fewer than five usable observations
- `recovering`: at least six usable observations, elevated activity and heart rate at the start, followed by lower average heart rate and activity near the end
- `resting`: average activity level below `0.25`
- `moderate activity`: average activity level from `0.25` up to but not including `0.67`
- `high activity`: average activity level `0.67` or higher

Recovery detection compares the first three usable observations with the last three usable observations. At the start, average activity must be above `0.5` and average heart rate must be more than `20` beats per minute above the participant's baseline. Both average heart rate and average activity must then decrease toward the end.

## Output Files

The program creates the `output/` directory automatically and writes:

### `analysis_summary.csv`

Contains one row per analyzed session with session ID, participant ID, usable observation count, classification, and selected average values.

### `analysis_report.txt`

Contains a readable section for each analyzed session, including baseline values, total and usable observations, classification, explanation, and summary statistics.

### `rejected_records.txt`

Lists rejected session rows with the source filename, row number, field, and reason.

The files are opened in write mode, so running the program again produces predictable output without requiring manual cleanup.

## Running the Program

Run from the repository root:

```bash
python main.py
```

The default command reads:

- `data/participants.csv`
- `data/fitness_sessions.csv`
- `data/fitness_sessions_invalid.csv`

and writes output to `output/`.

The same paths can be supplied explicitly:

```bash
python main.py --profiles data/participants.csv --sessions data/fitness_sessions.csv data/fitness_sessions_invalid.csv --output output
```

On systems that use `python3`, use `python3` instead of `python`.

The program prints a short completion summary showing accepted rows, rejected rows, and the created report files.

## Testing

Run the tests from the repository root:

```bash
python tests.py
```

The tests cover:

- valid input
- invalid input
- missing-file handling
- boundary values
- participant and session identifier validation
- custom exceptions
- session classifications

The tests read the official CSV files but do not modify them.

## Requirements

No third-party packages are required. The project uses only the Python standard library.
