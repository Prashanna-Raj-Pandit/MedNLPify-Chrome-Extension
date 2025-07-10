<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://foot-balance-nepal.vercel.app/">
    <img src="static/images/logo.png" alt="Logo" width="300" height="100">
  </a>

  <h3 align="center">MedNLPify</h3>

  <p align="center">
    An AI-powered Medical Abstract Classifier
    <br />
    <a href="https://github.com/Prashanna-Raj-Pandit/FootBalance-Nepal/tree/main/static/files"><strong>Checkout the models »</strong></a>
    <br />
    <br />
  </p>
</div>




<!-- ABOUT THE PROJECT -->
## About The Project

![img.png](static/images/web.png)

MedNLPify is a Chrome extension and NLP tool that simplifies the language of medical research abstracts to make them
more readable and accessible to non-experts and medical practitioners alike. It replicates and builds on the approach 
introduced in the paper <a href="https://arxiv.org/pdf/1612.05251">PubMed 200k RCT: a Dataset for Sequential Sentence Classification in Medical Abstracts</a>, 
using a trained NLP model to tag and classify sentences in medical abstracts.


 🚀Features
* Classifies sentences in medical abstracts into logical sections (e.g., Background, Objective, Method, Result, Conclusion).
* Enhances readability by helping users understand the structure and flow of research papers.
*  Chrome extension integration for real-time simplification of abstracts on PubMed or similar research databases.
* Powered by NLP and Deep Learning using TensorFlow 

### Built With

<p float="left">
  <a href="https://developer.mozilla.org/en-US/docs/Web/HTML">
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  </a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/CSS">
    <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  </a>
  <a href="https://flask.palletsprojects.com/">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  </a>
  <a href="https://www.tensorflow.org/">
    <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" />
  </a>
  <a href="https://keras.io/">
    <img src="https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white" />
  </a>
  <a href="https://scikit-learn.org/">
    <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  </a>
</p>



### Model Architecture

<p float="left">
  <img src="images/img.png" width="45%" />
  <img src="https://github.com/user-attachments/assets/b9670b17-2d50-4d24-be8d-22997a27c7d5" width="45%" />
</p>

1. Create a token-level model (similar to model_1)
2. Create a character-level model (similar to model_3 with a slight modification to reflect the paper)
3. Create a "line_number" model (takes in one-hot-encoded "line_number" tensor and passes it through a non-linear layer)
4. Create a "total_lines" model (takes in one-hot-encoded "total_lines" tensor and passes it through a non-linear layer)
5. Combine (using layers.Concatenate) the outputs of 1 and 2 into a token-character-hybrid embedding and pass it series of output to Figure 1 and section 4.2 of Neural Networks for Joint Sentence Classification in Medical Paper Abstracts
6. Combine (using layers.Concatenate) the outputs of 3, 4 and 5 into a token-character-positional tribrid embedding
7. Create an output layer to accept the tribrid embedding and output predicted label probabilities
8. Combine the inputs of 1, 2, 3, 4 and outputs of 7 into a tf.keras.Model

![img_1.png](img_1.png)

**Model Comparison**
<img src="static/images/model_comparison.png"></img>
<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## References
1. PubMed 200k RCT: A Dataset for Sequential Sentence Classification in Medical Abstracts
* Authors: Franck Dernoncourt, Ji Young Lee
* arXiv: https://arxiv.org/abs/1710.06071
* GitHub: https://github.com/Franck-Dernoncourt/pubmed-rct

2. mrdbourke-tensorflow-deep-learning