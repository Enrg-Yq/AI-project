from neo4j import GraphDatabase
from openai import OpenAI
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())


class EmbeddingGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("BASE_URL")
        )
    def generate_embedding(self,text):
        response = self.client.embeddings.create(
            model="embedding-3",
            dimensions = 1536,
            input=text
        )
        return response.data[0].embedding
    # query：必需参数，是一个字符串类型的 Cypher 查询语句，用于指定要在数据库中执行的操作。
    # params：可选参数，默认值为 None，是一个字典类型，用于传递查询所需的参数。
    # db_name：可选参数，默认值为 "neo4j"，表示要连接的数据库名称。
def neo4j_query(query, params=None, db_name="neo4j"):
    # 使用 with 语句确保数据库连接在使用完毕后自动关闭
    with GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", "12345678")
    ) as driver:
        # 执行查询
        results, _, _ = driver.execute_query(query, params, database=db_name)
        return results

if __name__=="__main__":
    emb = EmbeddingGenerator()
    search_query = "MATCH (n:Movie) RETURN n "
    update_query = """
    MATCH (n:Movie)
    WHERE elementId(n) = $element_id
    CALL db.create.setNodeVectorProperty(n,'embedding',$embedding)
    YIELD node
    RETURN node
    """
    # 'embedding'给节点 n 设置一个名为 embedding 的属性。
    # 先通过 MATCH (n:Movie) RETURN n 查询出所有 Movie 类型的节点，接着遍历这些节点，
    # 为每个节点生成对应的嵌入向量 embedding，最后借助 neo4j_query 函数执行 update_query，
    # 调用 db.create.setNodeVectorProperty 存储过程，把嵌入向量作为属性值设置到对应的节点上。
    results = neo4j_query(search_query)

    for record in results:
  
        print ('title',record['n']['title'])
        # print ('tagline:',record['n']['tagline'])
        print (record['n'].element_id)

        movie_info = f"{record['n']['title']}:{record['n']['tagline']}"
        embedding = emb.generate_embedding(movie_info)

        params = {"element_id":record['n'].element_id,
                  "embedding":embedding}
        
        result = neo4j_query(update_query,params)

        print(len(embedding))
        print("更新的节点数量:", result[0]["updated"] if result else 0)



    