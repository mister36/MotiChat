from rasa.shared.core.slots import Slot

class SentimentScoreSlot(Slot):

    def feature_dimensionality(self):
        return 3

    def as_feature(self):
        r = [0.0] * self.feature_dimensionality()
        if self.value:
            # Very neg (1, 0, 0)
            if -1.0 <= self.value <= -0.5:
                r = (1, 0, 0)
            # Slightly neg (0, 1, 0)
            elif -0.5 < self.value <= -0.05:
                r = (0, 1, 0)
            # Neutral (0, 0, 1)
            elif -0.05 < self.value <= 0.05:
                r = (0, 0, 1)
            # Slightly pos (1, 1, 0)
            elif 0.05 < self.value <= 0.5:
                r = (1, 1, 0)
            # Very pos (0, 1, 1)
            elif 0.5 < self.value <= 1.0:
                r = (0, 1, 1)
        return r