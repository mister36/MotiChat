import typing
from typing import Any, Optional, Text, Dict, List, Type

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.constants import TEXT

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata

import nltk
nltk.download('vader_lexicon')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

class SentimentAnalyzer(Component):
    """VADER sentiment component"""

    # provides = ["entities"]

    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        """Specify which components need to be present in the pipeline."""

        return []

    defaults = {}
    supported_language_list = ["en"]

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)

    # def __init__(self, component_config=None):
    #     super(SentimentAnalyzer, self).__init__(component_config)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any) -> None:
        """Not needed, because the the model is pretrained"""
        pass



    def convert_to_rasa(self, value, confidence, start, end):
        """Convert model output into the Rasa NLU compatible output format."""
        
        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "sentiment",
                  "start": start,
                  "end": end,
                  "extractor": "SentimentExtractor"}

        return entity


    def process(self, message: Message, **kwargs: Any) -> None:
        """Retrieve the text message, pass it to the classifier
            and append the prediction results to the message class."""
        sid = SentimentIntensityAnalyzer()
        
        res = sid.polarity_scores(message.get('text', default='test'))
        compound_score = res['compound']

        entity = self.convert_to_rasa(compound_score, 1, 0, len(message.get('text', default="test")))

        message.set("entities", [entity], add_to_output=True)


    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        pass

    @classmethod
    def load(cls, meta: Dict[Text, Any], model_dir: Optional[Text] = None, model_metadata: Optional["Metadata"] = None, cached_component: Optional["Component"] = None, **kwargs: Any) -> "Component":
        """Load this component from file."""

        if cached_component:
            return cached_component
        else:
            return cls(meta)