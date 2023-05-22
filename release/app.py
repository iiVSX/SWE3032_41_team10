from flask import Flask, render_template, request, make_response
import torch
import pymysql
import numpy as np
import pandas as pd
from transformers import ElectraForSequenceClassification, ElectraTokenizer

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    tel = request.form['tel']
    sentiment = request.form['sentiment']

    user_id = register_user(name, tel)

    label, probs = get_emotion_prob(sentiment)
    candidates = get_canidates(label)
    similarity, id, title = recommend(probs, candidates)
    similarity = int(similarity * 100)

    save_id = save_result(user_id, id, label, probs)

    return render_template('result.html', similarity=similarity, title=title, id=save_id)


@app.route('/save', methods=['POST'])
def save():
    is_satisfied = request.form['is_satisfied']
    save_id = request.form['id']

    feedback(save_id, is_satisfied)

    return render_template('result.html', similarity=similarity, id=id, title=title, user_id=user_id)


def get_emotion_prob(text):
    # 입력된 문장을 토큰화
    inputs = tokenizer(text, return_tensors="pt")

    # GPU 사용 여부에 따라 입력을 적절한 장치로 이동
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # 모델에 입력값을 넣고 예측
    outputs = model(**inputs)
    logits = outputs.logits

    # 예측 결과를 softmax 함수를 이용하여 확률값으로 변환
    probs = torch.nn.functional.softmax(logits, dim=-1)

    # 확률값 중에서 가장 큰 값의 인덱스를 예측 클래스로 사용
    pred_class = torch.argmax(probs, dim=-1)

    # 확률값 및 예측 클래스 출력
    class_dict = {0: 'happiness', 1: 'sadness', 2: 'fear', 3: 'neutral', 4: 'anger', 5: 'disgust', 6: 'surprised'}

    return class_dict[pred_class], probs.tolist()[0]


def recommend(probs, candidates):
    m_probs = np.vstack((candidates['happiness'], candidates['sadness'], candidates['fear', candidates['neutral'], candidates['anger'], candidates['disgust'], candidates['surprised']]))
    m_probs = np.transpose(m_probs)
    similarities = [(cos_sim(probs, mp), i) for i, mp in enumerate(m_probs)]
    similarity, m_idx = max(similarities)

    title = candidates['title'][m_idx]
    id = candidates['id'][m_idx]

    return similarity, id, title


def get_candidates(label):
    sql = "SELECT id, title, label, happiness, sadness, fear, neutral, anger, disgust, surprised FROM music WHERE label="
    sql += label
    rows = query(sql)

    candidates = pd.DataFrame(rows)
    return candidates


def register_user(name, tel):
    sql_format = "INSERT INTO user (name, tel) VALUES ('{name}', '{tel}')"
    sql = sql_format.format(name=name, tel=tel)
    rows = query(sql)
    sql = "SELECT LAST_INSERT_ID()"
    rows = query(sql)
    return rows[0]


def save_result(user_id, music_id, label, probs):
    sql_format = "INSERT INTO 0_user (user_id, label, happiness, sadness, fear, neutral, anger, disgust, surprised, music_id) " \
                 "VALUES('{user_id}', '{label}', '{happiness}', '{sadness}', '{fear}', '{neutral}', '{anger}', '{disgust}', '{surprised}', '{music_id}')"

    sql = sql_format.format(user_id=user_id, label=label, happiness=probs[0], sadness=probs[1], fear=probs[2], neutral=probs[3],
                            anger=probs[4], disgust=probs[5], suprised=probs[6], music_id=music_id)
    rows = query(sql)
    sql = "SELECT LAST_INSERT_ID()"
    rows = query(sql)
    return rows[0]


def feedback(save_id, is_satisfied):
    sql_format = "UPDATE 0_user SET is_satisfied='{is_satisfied}' WHERE id='{id}'"
    sql = sql_format.format(is_satisfied=is_satisfied, id=save_id)
    rows = query(sql)


def query(sql):
    con = pymysql.connect(host='#', user='root',
                          password='#',
                          db='main', charset='utf8')
    with con:
        with con.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            con.commit()

    return rows


def load():
    model_directory = '/home/ubuntu/model'
    pre_trained_model = ElectraForSequenceClassification.from_pretrained(model_directory, num_labels=7, local_files_only=True)
    pre_trained_model.to(device)

    tokenizer_directory = '/home/ubuntu/tokenizer'
    pre_trained_tokenizer = ElectraTokenizerFast.from_pretrained(tokenizer_directory, local_files_only=True)
    return pre_trained_model, pre_trained_tokenizer


@app.route('/test')
def test():
    rows = query("SELECT * FROM music")
    print(rows)
    return make_response("Success", 200)


if __name__ == '__main__':
    device = 'cpu'
    model, tokenizer = load()
    app.run('0.0.0.0', port=5000, debug=True)
