import requests
import json
import logging as log
log.basicConfig(level=log.INFO)


def multiply_two_numbers(a,b):
    result=a*b
    return result

def add_two_numbers(a,b):
    result=a+b
    return result

def baidu_search(query):
    log.info(f"开始搜索：{query}")
    uri = "https://qianfan.baidubce.com/v2/ai_search"
    headers = {
        "Authorization": "Bearer bce-v3/ALTAK-FkMPbGRHfcip55Qh9Ufkm/c1bd381d810edcd525845c8dfbef8807cbe429b2",
        "Content-Type": "application/json"
    }
    reponse = requests.post(
        uri,
        json={
            "messages": [{"role": "user", "content": query}],
        },
        headers=headers,

    )
    results = json.loads(reponse.text)
    return f'{results["references"]}'

MULTIPLY_TWO_NUMBERS = 2
ADD_TWO_NUMBERS =1
BAIDU_SEARCH = {
    "type": "function",
    "function": {
        "name": "baidu_search",
        "description": "使用百度搜索工具进行搜索",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词"
                }
            },
            "required": ["query"]
        }
    }
}


# multiply_two_numbers ，add_two_numbers 没写
