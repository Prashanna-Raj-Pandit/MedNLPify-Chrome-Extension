import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings

from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import spacy
from spacy.lang.en import English

app = Flask(__name__)

# Initialize spaCy with sentencizer
nlp = English()
nlp.add_pipe("sentencizer")


# Custom USE Wrapper Layer with proper serialization
from keras.saving import register_keras_serializable

@register_keras_serializable(package="Custom")
class USEWrapper(tf.keras.layers.Layer):
    def __init__(self, trainable=False, **kwargs):
        super().__init__(trainable=trainable, **kwargs)
        self.use = None

    def build(self, input_shape):
        self.use = hub.KerasLayer(
            "https://tfhub.dev/google/universal-sentence-encoder/4",
            trainable=self.trainable
        )

    def call(self, inputs):
        return self.use(inputs)

    def get_config(self):
        config = super().get_config()
        return config

# Load model with custom objects
try:
    model = tf.keras.models.load_model(
        'Model5_tribrid.keras',
        custom_objects={'USEWrapper': USEWrapper}
    )
except Exception as e:
    raise Exception(f"Error loading model: {e}")

# Label encodings (must match your model's training order)
LABEL_ENCODINGS = [
    'BACKGROUND',
    'CONCLUSIONS',
    'METHODS',
    'OBJECTIVE',
    'RESULTS'
]


def preprocess_text(text):
    """Split text into sentences using spaCy"""
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def split_sentences(text):
    """Split sentences into characters"""
    return " ".join(list(text))


def predict_abstract(abstract):
    """Predict labels for each sentence in the abstract"""
    sentences = preprocess_text(abstract)
    total_lines = len(sentences)

    # Prepare line number features
    line_numbers = list(range(total_lines))
    line_numbers_one_hot = tf.one_hot(line_numbers, depth=15)

    # Prepare total lines features
    total_lines_one_hot = tf.one_hot([total_lines - 1] * total_lines, depth=20)

    # Prepare character-level features
    abstract_chars = [split_sentences(sent) for sent in sentences]

    # Make predictions
    predictions = model.predict((
        line_numbers_one_hot,
        total_lines_one_hot,
        tf.constant(sentences),
        tf.constant(abstract_chars)
    ))

    predicted_labels = [np.argmax(pred) for pred in predictions]
    return sentences, [LABEL_ENCODINGS[i] for i in predicted_labels]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/classify', methods=['POST'])
def classify():
    abstract = request.form['abstract']
    sentences, labels = predict_abstract(abstract)

    results = [{
        'text': sent,
        'label': label,
        'class': f"label-{label}"
    } for sent, label in zip(sentences, labels)]

    return jsonify({'result': results})


if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request, jsonify
# import tensorflow as tf
# import numpy as np
# from keras.preprocessing.sequence import pad_sequences
# import json
# import spacy
# from spacy.lang.en import English
# nlp=English()
# sentensizer=nlp.add_pipe("sentencizer")
# app = Flask(__name__)
#
# try:
#     model = tf.keras.models.load_model('Model5_tribrid.keras')
# except Exception as e:
#     raise Exception(e)
# nlp = spacy.load("en_core_web_sm")
#
# LABEL_ENCODINGS = [
#     'BACKGROUND',
#     'CONCLUSIONS',
#     'METHODS',
#     'OBJECTIVE',
#     'RESULTS'
# ]
#
# def preprocess_text(text):
#     doc = nlp(text)
#     sentences = [sent.text for sent in doc.sents]
#     return sentences
# # Function to split sentences into characters
# def split_sentences(text):
#     return " ".join(list(text))
# def predict_abstract(abstract):
#     sentences = preprocess_text(abstract)
#     total_lines_in_test_abstract=len(sentences)
#     sample_lines=[]
#     for i, line in enumerate(sentences):
#         test_dict={}
#         test_dict["text"]=str(line)
#         test_dict["line_number"]=i
#         test_dict["total_lines"]=total_lines_in_test_abstract-1
#         sample_lines.append(test_dict)
#
#     test_abstract_line_number=[line["line_number"] for line in sample_lines]
#     test_abstract_line_number_one_hot=tf.one_hot(test_abstract_line_number,depth=15)
#
#     # Get total lines one hot encoded
#     test_abstract_total_lines=[line["total_lines"] for line in sample_lines]
#     test_abstract_total_lines_one_hot=tf.one_hot(test_abstract_total_lines,depth=20)
#     # split chars
#     abstract_chars=[split_sentences(sentence) for sentence in sentences]
#
#     test_abstract_preds=model.predict(x=(test_abstract_line_number_one_hot,test_abstract_total_lines_one_hot,
#                                          tf.constant(sentences), tf.constant(abstract_chars)))
#     abstract_class_preds=tf.argmax(test_abstract_preds,axis=1)
#     classes=[LABEL_ENCODINGS[i] for i in abstract_class_preds]
#     return  sentences,classes
#
# @app.route('/')
# def home():
#     return render_template('index.html')
#
# @app.route('/classify', methods=['POST'])
# def classify():
#     abstract = request.form['abstract']
#     print(abstract)
#     sentences, labels = predict_abstract(abstract)
#     labeled_sentences = [{
#         'text': sent,
#         'label': label,
#         'class': f"label-{label}"
#     } for sent, label in zip(sentences, labels)]
#
#     return jsonify({'result': labeled_sentences})
#
#
# if __name__ == '__main__':
#     app.run(debug=True)