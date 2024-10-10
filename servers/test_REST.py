import requests

def test_rest_api_server():
    # GET 요청 테스트
    response = requests.get('http://127.0.0.1:5000/api')
    if response.status_code == 200:
        print("GET Request Test Passed:", response.json())
    else:
        print("GET Request Test Failed")

    # POST 요청 테스트
    response = requests.post('http://127.0.0.1:5000/api', json={"key": "value"})
    if response.status_code == 200:
        print("POST Request Test Passed:", response.json())
    else:
        print("POST Request Test Failed")

if __name__ == "__main__":
    test_rest_api_server()

