from data_generator import generate_fitness_data
from models import Participant, Observation, Session
from analysis import analyze_session, print_report

profile, observations = generate_fitness_data(
    participant_id="P001",
    scenario="recovery",
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

session = Session(participant, valid_observations)

report = analyze_session(session, len(observations))
print_report(report)