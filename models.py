class Participant: 
    def __init__(self, participant_id, baseline_heart_rate, baseline_skin_response, baseline_temperature):
        self.participant_id=participant_id
        self.baseline_heart_rate=baseline_heart_rate
        self.baseline_skin_response=baseline_skin_response
        self.baseline_temperature=baseline_temperature

    @property
    def baseline_heart_rate(self):
        return self._baseline_heart_rate

    @baseline_heart_rate.setter
    def baseline_heart_rate(self, new_value):
        if new_value < 35 or new_value > 205:
            raise ValueError("Baseline heart rate must be between 35 and 205.")
        self._baseline_heart_rate = new_value

class Observation:
    def __init__(self, timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        self.timestamp=timestamp
        self.heart_rate=heart_rate
        self.skin_response=skin_response
        self.temperature=temperature
        self.activity_level=activity_level
        self.signal_quality=signal_quality

    def is_valid(self):
        # Check if observation values are within expected ranges 
        if self.timestamp is None or not isinstance(self.timestamp, int) or self.timestamp < 0:
            return False

        if self.heart_rate is None or not isinstance(self.heart_rate, (int, float)) or self.heart_rate < 35 or self.heart_rate > 205:
            return False

        if self.skin_response is None or self.skin_response < 0:
            return False

        if self.temperature is None or self.temperature < 25 or self.temperature > 42:
            return False

        if self.activity_level is None or self.activity_level < 0 or self.activity_level > 1:
            return False

        if (
            self.signal_quality is None
            or not isinstance(self.signal_quality, (int, float))
            or self.signal_quality < 0.60
            or self.signal_quality > 1
        ):
            return False

        return True
    

class Session: 
    def __init__(self, participant, observations):
        self.participant=participant
        self.observations=observations