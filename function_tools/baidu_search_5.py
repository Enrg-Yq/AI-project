import requests
import json

if __name__ == "__main__":
    uri = "https://qianfan.baidubce.com/v2/ai_search"
    headers = {
        "Authorization": "Bearer bce-v3/ALTAK-FkMPbGRHfcip55Qh9Ufkm/c1bd381d810edcd525845c8dfbef8807cbe429b2",
        "Content-Type": "application/json"
    }
    reponse = requests.post(
        uri,
        json={
            "messages": [{"role": "user", "content": "北京有哪些经典的景点？请用中文回答。"}],
        },
        headers=headers,

    )
    results = json.loads(reponse.text)
    for item in results["references"]:
        print(item['title'])
        print('-'*10)
        print(item['content'])