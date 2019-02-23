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


def getHitStore(stores):
    print(stores)
    return

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
                'iterationId': 'dd2e1505-5010-4814-90fe-d411a9b912e6',
            })
            data = ''
            try:
                conn = http.client.HTTPSConnection(
                    'southcentralus.api.cognitive.microsoft.com')
                #f = open("original.jpg", "rb", buffering=0)
                f = img_file.stream
                # conn.request("POST", "/customvision/v2.0/Prediction/a14c3964-9e4d-4cd8-b7fb-26b75796bd32/image?%s" %
                #              params, f.readall(), headers)
                conn.request("POST", "/customvision/v2.0/Prediction/a14c3964-9e4d-4cd8-b7fb-26b75796bd32/image?%s" %
                             params, f, headers)
                response = conn.getresponse()
                data = response.read()
                conn.close()
                stores = json.loads(data)
                getHitStore(stores['predictions'])
                print(stores)
            except Exception as e:
                # print("[Errno {0}] {1}".format(e.errno, e.strerror))
                print(e)

            # total = count_word(text)
            return render_template('main.html', sentence=data)

        else:
            return ''' <p>'png', 'jpg', 'gif' 以外のファイルはダメなんで</p> '''

    return render_template('main.html')


if __name__ == "__main__":
    app.run(debug=True)
