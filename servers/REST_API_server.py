from flask import Flask, request, jsonify

app = Flask(__name__)

# GET 요청에 대한 처리
@app.route('/api', methods=['GET'])
def api_get():
    return jsonify({"message": "This is a GET response", "data": "You successfully made a GET request!"})

# POST 요청에 대한 처리
@app.route('/api', methods=['POST'])
def api_post():
    data = request.json  # 클라이언트로부터 받은 JSON 데이터를 파싱
    return jsonify({"message": "This is a POST response", "received_data": data})

if __name__ == '__main__':
    # 서버 실행
    app.run(host='0.0.0.0', port=5002)  # REST API 서버는 5002번 포트에서 실행됨
