from flask import Flask, render_template, request
import joblib

app = Flask(__name__,static_url_path='/static')

# Load the model and TF-IDF vectorizer
loaded_model = joblib.load('TF-IDF_RF.pkl')
tfidf_vectorizer = joblib.load('vectorizer_TF-IDF.pkl')

def predict_url(url):
    # Vectorize the input URL using the loaded TF-IDF vectorizer
    url_vector = tfidf_vectorizer.transform([url])

    # Predict the label
    prediction = loaded_model.predict(url_vector)

    return "Malicious" if prediction[0] == 1 else "Benign"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        user_input = request.form['url']
        result = predict_url(user_input)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
