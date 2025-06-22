from neo4j import GraphDatabase
from openai import OpenAI


class EmbeddingGenerator:
    """
    文本嵌入生成器类
    用于将文本转换为向量形式的嵌入表示
    """
    def __init__(self):
        # 初始化OpenAI客户端
        # 使用阿里云的模型服务替代OpenAI
        # base_url指向阿里云的API端点
        self.client = OpenAI(
            api_key="sk-ea4f7f70ca2a4b4b9a11ba1608a6f777",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

    def generate_embedding(self, text):
        """
        生成文本的嵌入向量
        params:
            text: 需要转换的文本
        returns:
            返回1536维的向量表示
        """
        response = self.client.embeddings.create(
            model="text-embedding-v4",
            input=text,
            dimensions=1536,  # 指定嵌入维度为1536
        )
        return response.data[0].embedding


def neo4j_query(query, params=None, db_name="neo4j"):
    """
    执行Neo4j数据库查询的通用函数
    params:
        query: Cypher查询语句
        params: 查询参数字典
        db_name: 数据库名称
    returns:
        查询结果
    """
    # 创建到Neo4j数据库的连接
    driver = GraphDatabase.driver(
        "bolt://localhost:7687", auth=("neo4j", "liangchenglei")
    )

    # 执行查询并获取结果
    results, _, _ = driver.execute_query(query, params, database=db_name)

    # 关闭数据库连接
    driver.close()

    return results


if __name__ == "__main__":
    # 创建嵌入生成器实例
    emb = EmbeddingGenerator()

    # 查询电影节点的Cypher语句
    query = "MATCH (n:Movie) RETURN n LIMIT 10"
    results = neo4j_query(query)

    # 将生成的embedding存储到对应节点的Cypher语句
    # 使用Neo4j的向量操作函数db.create.setNodeVectorProperty
    embedding_query = """
        MATCH (n:Movie)
        WHERE elementId(n) = $element_id
        CALL db.create.setNodeVectorProperty(n, 'embedding', $embedding)
        RETURN count(*) as updated
    """

    # 遍历每个电影节点，生成并存储其嵌入向量
    for record in results:
        print(record)
        # 打印电影标题
        print(record["n"]["title"])
        # 打印节点的唯一标识符
        print(record["n"].element_id)

        # 将电影标题和标语组合成文本
        movie_info = f"{record['n']['title']}:{record['n']['tagline']}"
        # 生成文本的嵌入向量
        embedding = emb.generate_embedding(movie_info)
        print("embedding length:", len(embedding))

        # 准备更新节点的参数
        params = {"element_id": record["n"].element_id, "embedding": embedding}

        # 执行更新操作
        result = neo4j_query(embedding_query, params)

        print("---" * 10)
    
    # 打印成功更新的节点数量
    print("更新的节点数量:", result[0]["updated"] if result else 0)
