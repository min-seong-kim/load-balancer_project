from flask import Flask, jsonify, request

app = Flask(__name__)

# GET 요청 처리
@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!")

# POST 요청 처리
@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify(received=data)

# 서버 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

