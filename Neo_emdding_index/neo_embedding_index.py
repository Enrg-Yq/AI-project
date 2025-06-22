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
    
def  neo4j_query(query,params=None,db_name="neo4j"):
    # 建立数据库连接
    driver = GraphDatabase.driver(
        "bolt://localhost:7687",
        auth = ("neo4j","12345678")

    )
    # 执行cyper查询
    results,_,_,=driver.execute_query(query,params,database=db_name)
    driver.close()
    return results

if __name__=="__main__":
    emb = EmbeddingGenerator()
    search_query = "MATCH (n:Movie) RETURN n "
    update_query = """
    MATCH (n:Movie)
    WHERE elementId(n) = $element_id
    CALL db.create.setNodeVectorProperty(n,'embedding',$embedding)


    """
    results = neo4j_query(search_query)

    for record in results:
  
        print ('title',record['n']['title'])
        # print ('tagline:',record['n']['tagline'])
        print (record['n'].element_id)

        movie_info = f"{record['n']['title']}:{record['n']['tagline']}"
        embedding = emb.generate_embedding(movie_info)
        params = {"element_id":record['n'].element_id,
                  "embedding":embedding}
        results = neo4j_query(update_query,params)
        print(len(embedding))
        print('---'*10)



    