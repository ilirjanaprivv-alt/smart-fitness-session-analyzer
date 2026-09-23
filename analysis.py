class FitnessAnalyzer:

    @staticmethod
    def has_enough_data(observations):
        return len(observations) >= 5

    @staticmethod
    def falling_heart_rate_and_activity(session):
        observations = session.observations

        if len(observations) < 6:
            return False

        first_three = observations[:3]
        last_three = observations[-3:]

        first_heart_rates = []
        last_heart_rates = []

        first_activity_levels = []
        last_activity_levels = []

        for observation in first_three:
            first_heart_rates.append(observation.heart_rate)
            first_activity_levels.append(observation.activity_level)

        for observation in last_three:
            last_heart_rates.append(observation.heart_rate)
            last_activity_levels.append(observation.activity_level)

        average_first_heart_rate = (
            sum(first_heart_rates) / len(first_heart_rates)
        )
        average_last_heart_rate = (
            sum(last_heart_rates) / len(last_heart_rates)
        )

        average_first_activity = (
            sum(first_activity_levels) / len(first_activity_levels)
        )
        average_last_activity = (
            sum(last_activity_levels) / len(last_activity_levels)
        )

        baseline = session.participant.baseline_heart_rate

        started_active = (
            average_first_activity > 0.5
            and average_first_heart_rate > baseline + 20
        )

        heart_rate_falling = (
            average_last_heart_rate < average_first_heart_rate
        )

        activity_falling = (
            average_last_activity < average_first_activity
        )

        return (
            started_active
            and heart_rate_falling
            and activity_falling
        )

    @staticmethod
    def classify_session(session):
        valid_observations = session.observations

        if not FitnessAnalyzer.has_enough_data(valid_observations):
            return "insufficient data"

        if FitnessAnalyzer.falling_heart_rate_and_activity(session):
            return "recovering"

        activity_summary = summarize_activity_level(valid_observations)
        avg_activity = activity_summary["average"]

        if avg_activity < 0.25:
            return "resting"
        elif avg_activity < 0.67:
            return "moderate activity"
        else:
            return "high activity"

    @staticmethod
    def explain_classification(session):
        classification = FitnessAnalyzer.classify_session(session)

        if classification == "recovering":
            return (
                "Heart rate and activity decreased toward "
                "the end of the session."
            )
        elif classification == "resting":
            return "The average activity level was low."
        elif classification == "moderate activity":
            return "The average activity level was in the moderate range."
        elif classification == "high activity":
            return "The average activity level was high."
        else:
            return "There were too few usable observations."
    


def summarize_heart_rate(observations):
    heart_rates = []
    for observation in observations:
        heart_rates.append(observation.heart_rate)

    return {
        "average": sum(heart_rates) / len(heart_rates),
        "minimum": min(heart_rates),
        "maximum": max(heart_rates)
    }

def summarize_skin_response(observations):
    skin_responses = []
    for observation in observations:
        skin_responses.append(observation.skin_response)

    return {
        "average": sum(skin_responses) / len(skin_responses),
        "minimum": min(skin_responses),
        "maximum": max(skin_responses)
    }

def summarize_temperature(observations):
    temperatures = []
    for observation in observations:
        temperatures.append(observation.temperature)

    return {
        "average": sum(temperatures) / len(temperatures),
        "minimum": min(temperatures),
        "maximum": max(temperatures)
    }

def summarize_activity_level(observations):
    activity_levels = []
    for observation in observations:
        activity_levels.append(observation.activity_level)

    return {
        "average": sum(activity_levels) / len(activity_levels),
        "minimum": min(activity_levels),
        "maximum": max(activity_levels)
    }

def summarize_signal_quality(observations):
    signal_qualities = []
    for observation in observations:
        signal_qualities.append(observation.signal_quality)

    return {
        "average": sum(signal_qualities) / len(signal_qualities),
        "minimum": min(signal_qualities),
        "maximum": max(signal_qualities)
    }


def compare_heart_rate_to_baseline(participant, observations):
    baseline = participant.baseline_heart_rate
    differences = []
    for observation in observations:
        differences.append(observation.heart_rate - baseline)
    return differences

def compare_skin_response_to_baseline(participant, observations):
    baseline = participant.baseline_skin_response
    differences = []
    for observation in observations:
        differences.append(observation.skin_response - baseline)
    return differences

def compare_temperature_to_baseline(participant, observations):
    baseline = participant.baseline_temperature
    differences = []
    for observation in observations:
        differences.append(observation.temperature - baseline)
    return differences

def analyze_session(session, total_observations):
    report = {
        "participant_id": session.participant.participant_id,

        "baseline_heart_rate": session.participant.baseline_heart_rate,
        "baseline_skin_response": session.participant.baseline_skin_response,
        "baseline_temperature": session.participant.baseline_temperature,

        "total_observations": total_observations,
        "usable_observations": len(session.observations),

        "classification": FitnessAnalyzer.classify_session(session),
        "classification_reason": FitnessAnalyzer.explain_classification(session),
    }

    # Only calculate summaries if we have valid observations
    if len(session.observations) > 0:
        report["heart_rate_summary"] = summarize_heart_rate(
            session.observations
        )

        report["skin_response_summary"] = summarize_skin_response(
            session.observations
        )

        report["temperature_summary"] = summarize_temperature(
            session.observations
        )

        report["activity_level_summary"] = summarize_activity_level(
            session.observations
        )

        report["signal_quality_summary"] = summarize_signal_quality(
            session.observations
        )

        report["heart_rate_differences_from_baseline"] = (
            compare_heart_rate_to_baseline(
                session.participant,
                session.observations
            )
        )

        report["skin_response_differences_from_baseline"] = (
            compare_skin_response_to_baseline(
                session.participant,
                session.observations
            )
        )

        report["temperature_differences_from_baseline"] = (
            compare_temperature_to_baseline(
                session.participant,
                session.observations
            )
        )

    return report

def print_report(report):
    print("\n--- FITNESS SESSION REPORT ---")

    print("\nParticipant:")
    print("Participant ID:", report["participant_id"])
    print("Baseline Heart Rate:", report["baseline_heart_rate"])
    print("Baseline Skin Response:", report["baseline_skin_response"])
    print("Baseline Temperature:", report["baseline_temperature"])

    print("\nObservations:")
    print("Total Observations:", report["total_observations"])
    print("Usable Observations:", report["usable_observations"])

    print("\nClassification:")
    print(report["classification"])
    print("Explanation:", report["classification_reason"])

    # If there are no usable observations, there are no summaries to print
    if report["usable_observations"] == 0:
        print("\nNot enough valid data to calculate summaries.")
        return

    print("\nHeart Rate:")
    print("Average:", round(report["heart_rate_summary"]["average"], 2))
    print("Minimum:", report["heart_rate_summary"]["minimum"])
    print("Maximum:", report["heart_rate_summary"]["maximum"])

    print("\nSkin Response:")
    print("Average:", round(report["skin_response_summary"]["average"], 2))
    print("Minimum:", report["skin_response_summary"]["minimum"])
    print("Maximum:", report["skin_response_summary"]["maximum"])

    print("\nTemperature:")
    print("Average:", round(report["temperature_summary"]["average"], 2))
    print("Minimum:", report["temperature_summary"]["minimum"])
    print("Maximum:", report["temperature_summary"]["maximum"])

    print("\nActivity Level:")
    print("Average:", round(report["activity_level_summary"]["average"], 2))
    print("Minimum:", report["activity_level_summary"]["minimum"])
    print("Maximum:", report["activity_level_summary"]["maximum"])

    print("\nSignal Quality:")
    print("Average:", round(report["signal_quality_summary"]["average"], 2))
    print("Minimum:", report["signal_quality_summary"]["minimum"])
    print("Maximum:", report["signal_quality_summary"]["maximum"])
  