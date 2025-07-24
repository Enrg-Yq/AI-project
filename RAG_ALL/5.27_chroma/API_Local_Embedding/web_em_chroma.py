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

def llm_chat(messages):
    client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])
    result = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型编码
        messages=[{"role": "user", "content": messages}],
        temperature=0.4,
    )
    return result

if __name__ == '__main__':  
    
    load_dotenv()
    client = chromadb.HttpClient(host="localhost", port=8000)
    if not os.path.exists('127.0.0.1'):
        # 如果没有运行过chroma，就执行下面的操作，避免重复执行（生成的向量存入chroma，运行过chroma会有127.0.0.1文件）
        keywords,contents = parse_json('data_source.json')
        
        Embeddings = api_embedding(keywords,"embedding-3")
           
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

    question = input("请输入问题：")
    question_embedding = api_embedding([question],"embedding-3")
    collection = client.get_collection("RAG_Embedding")
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=2 
    )
    # print(results)
    if len(results['metadatas'])>0:
        content = results['metadatas'][0][0]['content']
        print("查询结果：", content)
    else:
        print("未找到相关内容。")

    prompt = f"你是一个精通python语言的编程专家，回答用户的问题。回答问题参考补充资料：{content}"
    print(prompt)

    answer = llm_chat(prompt)
    print(answer.choices[0].message.content)
    # print(answer.content)


