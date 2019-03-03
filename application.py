from flask import Flask, make_response, jsonify, render_template, request
import io
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import re
import json
# macOS + python3.6の組み合わせで起こるSSLに関するエラーの防止
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_store_name(store):
    store_name = store['tagName']
    return store_name


def get_probability(store):
    probability = store['probability']
    return probability

# '/' にget, postアクセスでhome()を通る
@app.route('/', methods=['POST', 'GET'])
def home():
    img_file = ''
    # ボタンを押した時(post)の処理
    if request.method == 'POST':
        if 'img_file' not in request.files:
            return render_template('main.html')

        img_file = request.files['img_file']

        if img_file and allowed_file(img_file.filename):
            headers = {
                # Request headers
                'Content-Type': 'multipart/form-data',
                'Prediction-key': '0f115d16825e47af8b61c98ede99124c',
            }

            params = urllib.parse.urlencode({
                # Request parameters
                'iterationId': '9ca5d1c2-be48-40ad-9117-4083843e6817',
            })
            data = ''
            try:
                conn = http.client.HTTPSConnection(
                    'southcentralus.api.cognitive.microsoft.com')
                f = img_file.stream
                conn.request("POST", "/customvision/v2.0/Prediction/a14c3964-9e4d-4cd8-b7fb-26b75796bd32/image?%s" %
                             params, f, headers)
                response = conn.getresponse()
                data = response.read()
                conn.close()
                stores = json.loads(data)
                store_name = get_store_name(stores['predictions'][0])
                probability = get_probability(stores['predictions'][0])
            except Exception as e:
                print(e)

            return render_template('main.html', sentence1='多分このお店でしょう。->', store_name=store_name,
                                   sentence2='確率：', probability=probability, )

        else:
            return ''' <p>'png', 'jpg', 'gif' 以外のファイルはダメなんで</p> '''

    return render_template('main.html')


if __name__ == "__main__":
    app.run(debug=True)
