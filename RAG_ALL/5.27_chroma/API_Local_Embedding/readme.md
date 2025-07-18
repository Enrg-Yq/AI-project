实现思路：
1. 数据加载读取，返回[{"keys":"干化词","content":"内容"}]
2. 调用API接口，实现Embedding
3. 调用本地模型，实现Embedding
4. chroma储存Embedding
4. 将用户问题转换成Embedding
5. 计算用户问题与知识库中每条数据的相似度
6. 对相似度进行排序，返回TopK条数据

