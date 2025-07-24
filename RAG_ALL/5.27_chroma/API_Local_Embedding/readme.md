实现思路：
1. 数据加载读取，返回[{"keys":"干化词","content":"内容"}]
2. 调用API接口，干化词、内容 实现Embedding
3. 调用本地模型，实现Embedding
4. chroma储存Embedding及文本内容
5. 查询：用户问题转换为Embedding，数据库查询相思度最高的TopK条数据
    5.1 将用户问题转换成Embedding
    5.2 计算用户问题Embedding与知识库中每条数据的相似度
    5.3 返回相似度最高的TopK条数据
6. 拼接到prompt中，调用本地模型，生成答案


# chroma 启动
# chroma run --path 127.0.0.1
