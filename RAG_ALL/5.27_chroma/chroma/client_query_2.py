import chromadb
import numpy as np

client = chromadb.HttpClient(host='localhost', port=8000)
# 如果一个`collection`已存在，那么获取它，如果不存在，则创建它：
collection = client.get_or_create_collection(name="collection2")

# 修正生成随机向量的代码，将参数改为元组
# embeddings = np.random.random((3, 384))
# collection.add(documents=['我是王小鱼','我们一起学习RAG','今晚学习chromadb'],
#                metadatas=[{'chapter':"3",'verse':'16'},{'chapter':"2",'verse':'10'},{'chapter':"5",'verse':'8'}],
#                embeddings= embeddings,
#                ids=['id1','id2','id3'],
#                )
# print(collection.peek())

# 查询向量
query = np.random.random((3, 384))

results = collection.query(
    query_embeddings=query,
    n_results=1,  # 返回最相似的1个文档
    # where={"keywords": "RAG"},  # 查询包含"RAG"的文档
)
print(results)