import chromadb
import numpy as np

client = chromadb.HttpClient(host='localhost', port=8000)
# 如果一个`collection`已存在，那么获取它，如果不存在，则创建它：
collection = client.get_or_create_collection(name="collection3")

# 指定向量
collection.add(documents=['我是王小鱼','我们一起学习RAG','今晚学习chromadb'],
               metadatas=[{'chapter':"3",'verse':'16'},{'chapter':"2",'verse':'10'},{'chapter':"5",'verse':'8'}],
               embeddings=[[-0.04291284,  0.12459736,  0.07283306],[0.00072299,  0.1379851 ,  0.05514374],[0.05965715,  0.06796112,  0.03112736]],
               ids=['id4','id5','id6'],
               )
print(collection.peek())

# 更新数据
collection.update(documents=['我是王小鱼','我们一起学习RAG','今晚学习chromadb'],
               metadatas=[{'chapter':"3",'verse':'16'},{'chapter':"2",'verse':'10'},{'chapter':"5",'verse':'8'}],
               embeddings=[[1.6,  1.2,  1.3],[0.00072299,  0.1379851 ,  0.05514374],[0.05965715,  0.06796112,  0.03112736]],
               ids=['id4','id5','id6'])

# 更新或插入数据
collection.upsert(documents=['王小鱼','RAG','chromadb'],
               metadatas=[{'chapter':"3",'verse':'16'},{'chapter':"2",'verse':'10'},{'chapter':"5",'verse':'8'}],
               embeddings=[[1.6,  1.2,  1.3],[0.00072299,  0.1379851 ,  0.05514374],[0.05965715,  0.06796112,  0.03112736]],
               ids=['id7','id8','id9'])


# 删除数据
collection.delete(ids=['id4'])
collection.delete(where={'chapter': '2'})


print(collection.peek())