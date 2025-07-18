import json
from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv
import chromadb

def parse_json(file_path):
    keywords,contents = [],[]
    # 读取文档
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            text = item['k_qa_content']
            key,content = text.split('#\n')            
            keywords.append(key)
            contents.append({'content': content})
    return keywords,contents

def api_embedding(texts,model_name):
    client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"]) 
    Embeddings = []
    for input_text in texts:
    
        response = client.embeddings.create(
            model=model_name, #填写需要调用的模型编码
            input=input_text,
            dimensions=512,
        )
        Embedding = response.data[0].embedding
        Embeddings.append(Embedding)
    return Embeddings

if __name__ == '__main__':  
    load_dotenv()
    processed_data = parse_json('data_source.json')
       
    keywords,contents = [],[]
    for item in processed_data:
        input_txt = item['key']
        input_content = item['content']

        keywords.append(input_txt)
        contents.append(input_content)

        Embeddings = api_embedding(keywords,"embedding-3")
        
    # print(len(Embeddings))

    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_or_create_collection("RAG_Embedding")
    
    ids = []
    for i in range(len(Embeddings)):
        ids.append(f"id{i+1}")

    collection.add(
        ids=ids,
        embeddings=Embeddings,
        documents=keywords,
        metadatas=contents,
    )
    print("数据已成功添加到 ChromaDB 中。")


# 1.20



