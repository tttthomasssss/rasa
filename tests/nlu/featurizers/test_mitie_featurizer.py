import numpy as np

from rasa.nlu.constants import (
    DENSE_FEATURE_NAMES,
    TEXT_ATTRIBUTE,
    RESPONSE_ATTRIBUTE,
    INTENT_ATTRIBUTE,
    TOKENS_NAMES,
)
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.tokenizers.mitie_tokenizer import MitieTokenizer
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.featurizers.dense_featurizer.mitie_featurizer import MitieFeaturizer


def test_mitie_featurizer(mitie_feature_extractor):

    featurizer = MitieFeaturizer.create({}, RasaNLUModelConfig())

    sentence = "Hey how are you today"
    tokens = MitieTokenizer().tokenize(sentence)

    vecs = featurizer.features_for_tokens(tokens, mitie_feature_extractor)

    expected = np.array(
        [0.00000000e00, -5.12735510e00, 4.39929873e-01, -5.60760403e00, -8.26445103e00]
    )
    expected_cls = np.array([0.0, -4.4551446, 0.26073121, -1.46632245, -1.84205751])

    assert 6 == len(vecs)
    assert np.allclose(vecs[0][:5], expected, atol=1e-5)
    assert np.allclose(vecs[-1][:5], expected_cls, atol=1e-5)


def test_mitie_featurizer_train(mitie_feature_extractor):

    featurizer = MitieFeaturizer.create({}, RasaNLUModelConfig())

    sentence = "Hey how are you today"
    message = Message(sentence)
    message.set(RESPONSE_ATTRIBUTE, sentence)
    message.set(INTENT_ATTRIBUTE, "intent")
    tokens = MitieTokenizer().tokenize(sentence)
    message.set(TOKENS_NAMES[TEXT_ATTRIBUTE], tokens)
    message.set(TOKENS_NAMES[RESPONSE_ATTRIBUTE], tokens)

    featurizer.train(
        TrainingData([message]),
        RasaNLUModelConfig(),
        **{"mitie_feature_extractor": mitie_feature_extractor},
    )

    expected = np.array(
        [0.00000000e00, -5.12735510e00, 4.39929873e-01, -5.60760403e00, -8.26445103e00]
    )
    expected_cls = np.array([0.0, -4.4551446, 0.26073121, -1.46632245, -1.84205751])

    vecs = message.get(DENSE_FEATURE_NAMES[TEXT_ATTRIBUTE])

    assert len(tokens) == len(vecs)
    assert np.allclose(vecs[0][:5], expected, atol=1e-5)
    assert np.allclose(vecs[-1][:5], expected_cls, atol=1e-5)

    vecs = message.get(DENSE_FEATURE_NAMES[RESPONSE_ATTRIBUTE])

    assert len(tokens) == len(vecs)
    assert np.allclose(vecs[0][:5], expected, atol=1e-5)
    assert np.allclose(vecs[-1][:5], expected_cls, atol=1e-5)

    vecs = message.get(DENSE_FEATURE_NAMES[INTENT_ATTRIBUTE])

    assert vecs is None
