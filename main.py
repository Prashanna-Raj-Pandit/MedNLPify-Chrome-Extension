from flask import Flask, render_template, request, jsonify
import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import json
# import spacy

app = Flask(__name__)
#
# # Load the model and tokenizer
# model = tf.keras.models.load_model('model/skimlit_model.h5')
# nlp = spacy.load("en_core_web_sm")
#
# # Load label encodings
# with open('model/label_encodings.json', 'r') as f:
#     label_encodings = json.load(f)
#

# Preprocessing functions
# def preprocess_text(text):
#     doc = nlp(text)
#     sentences = [sent.text for sent in doc.sents]
#     return sentences
#
#
# def predict_abstract(abstract):
#     sentences = preprocess_text(abstract)
#     tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
#     sequences = tokenizer.texts_to_sequences(sentences)
#     padded = pad_sequences(sequences, maxlen=20, padding="post", truncating="post")
#     predictions = model.predict(padded)
#     predicted_labels = [np.argmax(pred) for pred in predictions]
#     return sentences, predicted_labels
#

@app.route('/')
def home():
    return render_template('index.html')

#
# @app.route('/classify', methods=['POST'])
# def classify():
#     abstract = request.form['abstract']
#     sentences, labels = predict_abstract(abstract)
#
#     # Map numeric labels to class names
#     class_names = {int(k): v for k, v in label_encodings.items()}
#     labeled_sentences = [{
#         'text': sent,
#         'label': class_names[label],
#         'class': f"label-{label}"
#     } for sent, label in zip(sentences, labels)]
#
#     return jsonify({'result': labeled_sentences})


if __name__ == '__main__':
    app.run(debug=True)