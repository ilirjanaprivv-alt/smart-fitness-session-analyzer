# Smart Fitness Session Analyzer

**Selected option:** Option A – Smart Fitness Session Analyzer
**Student name:** Ilirijana Krasniqi
**Student number:** 385512

## Project Description

This project is a small object-oriented Python application for analyzing simulated fitness data from wearable sensors.

The program receives a participant profile and a list of sensor observations from the provided data generator. It converts the raw dictionaries into Python objects, validates the observations, calculates summary statistics, compares measurements with the participant's baseline values, classifies the fitness session, and prints a readable report.

The possible classifications are:

* resting
* moderate activity
* high activity
* recovering
* insufficient data

## Project Structure

```text
option_a_fitness/
│
├── README.md
├── main.py
├── models.py
├── analysis.py
├── data_generator.py
├── DATA_DESCRIPTION.md
├── example_usage.py
├── tests.py
└── requirements.txt
```

### `main.py`

The main entry point of the application.

It:

1. generates the raw fitness data;
2. creates a `Participant` object;
3. converts observation dictionaries into `Observation` objects;
4. removes observations that fail validation;
5. creates a `Session`;
6. analyzes the session; and
7. prints the final report.

### `models.py`

Contains the main domain classes used by the application:

* `Participant`
* `Observation`
* `Session`

### `analysis.py`

Contains the analysis logic, including:

* the `FitnessAnalyzer` class;
* summary calculations;
* comparisons with baseline values;
* recovery detection;
* session classification;
* creation of the structured result dictionary; and
* console report presentation.

### `data_generator.py`

Instructor-supplied file used to generate simulated participant profiles and sensor observations.

### `tests.py`

Contains tests for the five required scenarios:

* resting
* moderate activity
* high activity
* recovery
* poor-quality data

## Class Design

### `Participant`

Represents one participant and stores the participant's personal reference values:

* participant ID
* baseline heart rate
* baseline skin response
* baseline temperature

The baseline heart rate is controlled through a property and is used as an example of encapsulation.

### `Observation`

Represents one sensor observation window.

Each observation contains:

* timestamp
* heart rate
* skin response
* temperature
* activity level
* signal quality

The `is_valid()` method checks whether the observation contains usable sensor values.

### `Session`

Represents one complete fitness session.

A `Session` contains:

* one `Participant`
* a list of valid `Observation` objects

The class is also the main example of composition in the project.

### `FitnessAnalyzer`

Contains analysis-related behaviour that belongs to the analysis process rather than to one particular participant or observation.

The class currently contains the static method:

```python
FitnessAnalyzer.has_enough_data(observations)
```

This checks whether enough valid observations are available to classify the session.

A static method is used because this operation does not require access to a particular `FitnessAnalyzer` object or class-level state.

## Object-Oriented Design

### Composition

Composition is demonstrated by the `Session` class.

A session **has a** participant and **has many** observations.

```text
Session
├── Participant
└── Observation objects
```

Composition was preferred over inheritance because these objects do not have an "is-a" relationship.

For example:

* a `Session` is not a type of `Participant`;
* an `Observation` is not a type of `Session`;
* a `Participant` is not a type of `Observation`.

Instead, the objects naturally work together through "has-a" relationships.

### Encapsulation

Encapsulation is demonstrated in the `Participant` class with the protected-style attribute:

```python
_baseline_heart_rate
```

Access to this value is controlled through the `baseline_heart_rate` property.

The setter validates the value before storing it. A baseline heart rate outside the accepted range raises a `ValueError`.

### Inheritance and Method Overriding

Inheritance and method overriding are not used in this design.

Composition was considered a better fit because the domain objects have different responsibilities and do not form a meaningful parent-child or "is-a" relationship.

Introducing inheritance only to satisfy the requirement would make the design more complicated without improving the behaviour of the application.

## Validation Rules

Each `Observation` is checked before it is added to the session.

An observation is considered usable when:

* `timestamp` is an integer greater than or equal to `0`;
* `heart_rate` is between `35` and `205` beats per minute;
* `skin_response` is `0` or greater;
* `temperature` is between `25` and `42` degrees Celsius;
* `activity_level` is between `0` and `1`;
* `signal_quality` is between `0.60` and `1`.

A signal-quality threshold of `0.60` was chosen to reject measurements with very poor sensor reliability.

Invalid observations are excluded from the analysis.

## Summary Calculations

For the usable observations, the program calculates average, minimum, and maximum values for:

* heart rate;
* skin response;
* temperature;
* activity level; and
* signal quality.

The program also compares:

* heart rate with baseline heart rate;
* skin response with baseline skin response; and
* temperature with baseline temperature.

These comparisons are stored as differences from the participant's personal baseline.

## Classification Rules

### Insufficient data

A session is classified as `insufficient data` when fewer than five valid observations are available.

### Recovering

Recovery is checked before the normal activity classifications.

The program compares measurements near the beginning of the session with measurements near the end.

A session is considered to show recovery when:

* the participant started with elevated activity;
* the starting heart rate was clearly above the participant's baseline;
* average heart rate is lower near the end of the session; and
* average activity level is lower near the end of the session.

The implementation compares the first three usable observations with the last three usable observations to reduce the effect of one unusual measurement.

### Resting

If recovery is not detected, a session with:

```text
average activity level < 0.25
```

is classified as:

```text
resting
```

### Moderate activity

A session with:

```text
0.25 <= average activity level < 0.67
```

is classified as:

```text
moderate activity
```

### High activity

A session with:

```text
average activity level >= 0.67
```

is classified as:

```text
high activity
```

These thresholds are design assumptions used by this project and are intended for the supplied simulated data rather than real medical or fitness assessment.

## Structured Analysis Result

The analysis is returned as a Python dictionary.

The dictionary contains information such as:

* participant ID;
* baseline values;
* total number of observations;
* number of usable observations;
* classification;
* explanation of the classification;
* heart-rate summary;
* skin-response summary;
* temperature summary;
* activity-level summary;
* signal-quality summary; and
* differences from baseline values.

## Example Output

```text
--- FITNESS SESSION REPORT ---

Participant:
Participant ID: P001
Baseline Heart Rate: 78
Baseline Skin Response: 1.17
Baseline Temperature: 32.76

Observations:
Total Observations: 10
Usable Observations: 10

Classification:
recovering
Explanation: Heart rate and activity decreased toward the end of the session.

Heart Rate:
Average: 112.8
Minimum: 79
Maximum: 141

Skin Response:
Average: 1.56
Minimum: 1.3
Maximum: 1.93

Temperature:
Average: 33.03
Minimum: 32.73
Maximum: 33.34

Activity Level:
Average: 0.48
Minimum: 0.04
Maximum: 0.88

Signal Quality:
Average: 0.91
Minimum: 0.88
Maximum: 0.93
```

## Testing

The project includes tests for all five required scenarios.

Run the tests with:

```bash
python tests.py
```

The expected output is:

```text
Resting test passed.
Moderate activity test passed.
High activity test passed.
Recovery test passed.
Poor quality test passed.

All tests passed successfully.
```

The tests use a fixed random seed so that the generated data is reproducible.

## Installation and Running

This project only uses the Python standard library. No third-party packages are required.

Clone the repository:

```bash
git clone https://github.com/ilirjanaprivv-alt/smart-fitness-session-analyzer.git
```

Move into the repository:

```bash
cd smart-fitness-session-analyzer
```

Run the application:

```bash
python main.py
```

Run the tests with:

```bash
python tests.py
```

## Requirements

No external Python libraries are required.

The project uses only the Python standard library and the instructor-supplied data generator.

## Known Limitations

* The program analyzes simulated fitness data and is not intended for medical use.
* Classification thresholds are manually chosen for the supplied simulated dataset.
* Recovery detection uses a simple comparison between measurements near the beginning and end of a session.
* Invalid observations are excluded rather than repaired.
* The application uses console output only.
* The program does not use external APIs, databases, graphical interfaces, or machine-learning models.
