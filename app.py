from flask import Flask, request, jsonify, send_file
from tensorflow.keras.models import load_model
import pickle
from tensorflow.keras.preprocessing import sequence

PORT = 3000
app = Flask(__name__)

# Tải mô hình đã huấn luyện và tokenizer
model = load_model('model/GRU_model_v4.h5')
with open('model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

sequence_length = 100

# Hàm tiền xử lý văn bản
def prepare_data(X, tokenizer, sequence_length):
    X = tokenizer.texts_to_sequences(X)
    X = sequence.pad_sequences(X, maxlen=sequence_length)
    return X

# Route để dự đoán
@app.route('/api', methods=['POST'])
def predict():
    data = request.json['text']
    X = prepare_data([data], tokenizer, sequence_length)
    prediction = model.predict(X)
    y_pred = prediction.argmax(axis=-1)[0]
    return jsonify({'prediction': int(y_pred)})

@app.route('/', methods=['GET'])
def home():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=False, port=PORT)
