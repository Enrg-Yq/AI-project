from openai import OpenAI

if __name__ == '__main__':
    client = OpenAI(
        api_key="bce-v3/ALTAK-FkMPbGRHfcip55Qh9Ufkm/c1bd381d810edcd525845c8dfbef8807cbe429b2",
        base_url="https://qianfan.baidubce.com/v2/ai_search/",

    )
    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[
            {"role": "user",
             "content": "北京有哪些经典的景点？请用中文回答。"},

        ]
    )
    print(response.choices[0].message.content)
