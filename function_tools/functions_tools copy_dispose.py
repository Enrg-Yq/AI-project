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

def div_two_numbers(a,b):   
    log.info(f"除法运算：a={a},b={b}")
    if a==0:
        return "被除数不能为0"
    if b==0:
        return "除数不能为0"
    result=a/b
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

def huilv_search():
    log.info(f"汇率查询：") 
    # 基本参数配置
    apiUrl = 'http://web.juhe.cn/finance/exchange/frate'  # 接口请求URL
    apiKey = 'eb6bee402bb44eed82ece22711ee30a1'  # 在个人中心->我的数据,接口名称上方查看

    # 接口请求入参配置
    requestParams = {
        'key': apiKey,
        'type': '',
    }

    # 发起接口网络请求
    response = requests.get(apiUrl, params=requestParams)

    # 解析响应结果
    if response.status_code == 200:
        responseResult = response.json()
        # 网络请求成功。可依据业务逻辑和接口文档说明自行处理。
        print(responseResult)
    else:
        # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。
        print('请求异常')

def weather_search(city):
    log.info(f"天气查询：city={city}")
    api_key = "1fb39af1c5dda57a2eb386eaffd0e3ef"
    # 基本参数配置
    apiUrl = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}'
    response = requests.get(apiUrl)
    data = response.json()
    if response.status_code ==200:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        log.info(f'查询{city} 经度；{lat} 维度：{lon}')
    else:
        return '未查询到城市'
    base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.get(base_url)
    if response.requests.status == 200:
        data = response.json()
        log.info(f'查询{city} 天气：{data}')
        weather = {
                '温度': data['main']['temp'],
                '描述': data['weather'][0]['description'],
                '城市': data['name'],
                'country':data['sys']['country']
        }
        return weather
    else:
        return{"错误":data.get("message","an error occurred")}
    


MULTIPLY_TWO_NUMBERS = {
    "type": "function",
    "function": {
        "name": "multiply_two_numbers",
        "description": "两个数相乘",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "乘数"
                },
                "b": {
                    "type": "number",
                    "description": "被乘数"
                }
            },
            "required": ["a", "b"]
        }
    }
}

ADD_TWO_NUMBERS = {
    "type": "function",
    "function": {
        "name": "add_two_numbers",
        "description": "两个数相加",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "第一个加数"
                },
                "b": {
                    "type": "number",
                    "description": "第二个加数"
                }
            },
            "required": ["a", "b"]
        }
    }
}

DIV_TWO_NUMBERS = {
    "type": "function",
    "function": {
        "name": "div_two_numbers",
        "description": "两个数相除",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "被除数"},
                "b": {"type": "number", "description": "除数"}
            },
            "required": ["a", "b"]  # 说明两个参数是必须的
        }
    }
}

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

JUHE_SEARCH = {
    "type": "function",
    "function": {
        "name": "huilv_search",
        "description": "查询人民币与外币兑换的汇率",  
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

WEATHER_SEARCH = {
    "type": "function",
    "function": {
        "name": "weather_search",
        "description": "获取某个城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["city"]
        }   

    }
}
