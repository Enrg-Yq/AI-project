import json
from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv

def parse_json(file_path):
    processed_data = []
    # 读取文档
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            text = item['k_qa_content']
            key,content = text.split('#\n')
            processed_data.append({'key': key, 'content': content})
    return processed_data

def api_embedding(input_txt,client,model_name):
    response = client.embeddings.create(
        model=model_name, #填写需要调用的模型编码
        input=input_txt,
        dimensions=512,
    )
    Embedding = response.data[0].embedding
    
    return Embedding

if __name__ == '__main__':
    load_dotenv()
    processed_data = parse_json('data_source.json')
    # print(processed_data[0]) 
    client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])      
    
    Embeddings = []
    for item in processed_data:
        input_txt = item['key']
        
        Embedding = api_embedding(input_txt,client,"embedding-3")
        Embeddings.append(Embedding)
        # print(len(Embedding))
    print(Embeddings)
    # print(len(Embeddings))


