import chromadb
import numpy as np

client = chromadb.HttpClient(host='localhost', port=8000)
# 直接创建一个collection：
collection = client.create_collection(
    name="collection2",
    metadata={"hnsw:space": "cosine"} # l2 是默认值
)

# collection.add(documents=['我是王小鱼','我们一起学习RAG','今晚学习chromadb'],
#                metadatas=[{'chapter':"3",'verse':'16'},{'chapter':"2",'verse':'10'},{'chapter':"5",'verse':'8'}],
#                ids=['id1','id2','id3'],
#                )
# print(collection.peek())

# 修正生成随机向量的代码，将参数改为元组
embeddings = np.random.random((3, 384))
collection.add(documents=['我是王小鱼','我们一起学习RAG','今晚学习chromadb'],
               metadatas=[{'chapter':"3",'verse':'16'},{'chapter':"2",'verse':'10'},{'chapter':"5",'verse':'8'}],
               embeddings= embeddings,
               ids=['id1','id2','id3'],
               )
print(collection.peek())

# 删除一个collection
# client.delete_collection(name="my_collection")

# collections = client.list_collections()
# print(collections)