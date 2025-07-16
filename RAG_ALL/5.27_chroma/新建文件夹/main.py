import json
from zhipuai import ZhipuAI
import os
from modelscope import AutoTokenizer, AutoModel
import torch
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

def local_embedding(sentences):

    tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-large-zh-v1.5')
    model = AutoModel.from_pretrained('BAAI/bge-large-zh-v1.5')
    model.eval()

    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    with torch.no_grad():
        model_output = model(**encoded_input)
        sentence_embeddings = model_output[0][:, 0]

    sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
    return sentence_embeddings.numpy().tolist()

if __name__ == '__main__':
    load_dotenv()
    processed_data = parse_json('data_source.json')
    # print(processed_data[0]) 
    client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])      
    
    Embeddings = []
    keywords = []
    for item in processed_data:
        input_txt = item['key']
        
        # API调用
        # Embedding = api_embedding(input_txt,client,"embedding-3")
        # Embeddings.append(Embedding)
        
        # 本地调用
        keywords.append(input_txt)
    Embeddings = local_embedding(keywords)




    print(Embeddings)
    # print(len(Embeddings))


