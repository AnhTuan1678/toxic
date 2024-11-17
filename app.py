import os
import gdown
from flask import Flask, request, jsonify, send_file
from tensorflow.keras.models import load_model
import pickle
from tensorflow.keras.preprocessing import sequence
import numpy as np
import re
from pyvi.ViTokenizer import ViTokenizer
from text_preprocess import text_preprocess

# Mở và đọc file vn_offensive_words.txt
file_path = "vn_offensive_words.txt"
offensive_words = []

# Đọc từng dòng trong file
with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        word = line.strip()
        if word and not word.startswith("#"):
            offensive_words.append(word)


def contains_offensive_word(sentence, offensive_words):
    """
    Kiểm tra câu đầu vào có chứa từ nhạy cảm hay không.
    :param sentence: Chuỗi câu cần kiểm tra.
    :param offensive_words: Danh sách các từ nhạy cảm.
    :return: True nếu chứa từ nhạy cảm, False nếu không.
    """
    pattern = r"\b(?:" + "|".join(map(re.escape, offensive_words)) + r")\b"
    if re.search(pattern, sentence, flags=re.IGNORECASE):
        return True
    return False


def deEmojify(text):
    regrex_pattern = re.compile(
        pattern="["  # emoticons, symbols & pictographs, transport & map symbols, flags (iOS)
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE,
    )
    return regrex_pattern.sub(r"", text)


def preprocess(text, tokenized=True, lowercased=True):
    text = text_preprocess(text)
    text = ViTokenizer.tokenize(text) if tokenized else text
    text = deEmojify(text)
    text = text.lower() if lowercased else text
    return text


def pre_process_features(X, y, tokenized=True, lowercased=True):
    X = [
        preprocess(str(p), tokenized=tokenized, lowercased=lowercased) for p in list(X)
    ]
    X = [x for x in X if x]  # Lọc bỏ các phần tử rỗng
    y = [y[i] for i in range(len(X))]  # Đồng bộ với y
    return X, y


def prepare_data(X, tokenizer, sequence_length):
    X = tokenizer.texts_to_sequences(X)
    X = sequence.pad_sequences(X, maxlen=sequence_length)
    return X


PORT = 3000
app = Flask(__name__)


# Kiểm tra xem tệp mô hình và tokenizer có tồn tại không, nếu chưa có thì tải về
def download_files():
    model_path = "model/GRU_model_v4.h5"
    tokenizer_path = "model/tokenizer.pickle"

    # Tạo thư mục 'model' nếu chưa có
    if not os.path.exists("model"):
        os.makedirs("model")

    if not os.path.exists(model_path):
        model_url = "https://drive.google.com/uc?id=1vCdpvh6L1SVl7wVJrjinLmJyohyGw1ew"  # Thay bằng ID thật của bạn
        gdown.download(model_url, model_path, quiet=False)

    # https://drive.google.com/file/d/1cGK79nJN1MaawQQWluCTo3vcC96KLB5B/view?usp=sharing
    if not os.path.exists(tokenizer_path):
        tokenizer_url = "https://drive.google.com/uc?id=1cGK79nJN1MaawQQWluCTo3vcC96KLB5B"  # Thay bằng ID thật của bạn
        gdown.download(tokenizer_url, tokenizer_path, quiet=False)


# Tải mô hình và tokenizer nếu chưa có
download_files()

# Tải mô hình đã huấn luyện và tokenizer
model = load_model("model/GRU_model_v4.h5")
with open("model/tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)
sequence_length = 100


@app.route("/api", methods=["POST"])
def predict():
    data = request.json["text"]
    if contains_offensive_word(data, offensive_words):
        return jsonify({"prediction": 1})
    X, _ = pre_process_features([data], [0])
    X = prepare_data(X, tokenizer, sequence_length)
    prediction = model.predict(X)
    y_pred = prediction.argmax(axis=-1)[0]
    return jsonify({"prediction": int(y_pred)})


@app.route("/", methods=["GET"])
def home():
    return send_file("index.html")


if __name__ == "__main__":
    app.run(debug=False, port=PORT)
