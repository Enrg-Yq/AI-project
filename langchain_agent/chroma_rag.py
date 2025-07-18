from langchain_community.document_loaders import PDFMinerLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

class MyChroma(Chroma):
    def add_file(self,filename):
        """
        Add a PDF filt to Chroma collection.
        Parameters:
        ---------
        :param filename: Path to the PDF file.     
        
        """
        doculment = PDFMinerLoader(filename).load()
        splits = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200).split_documents(doculment)
        self.add_documents(splits)

    @classmethod
    def add_folder(cls,persist_directory,collection_name,folder_path):
        embedding_function = OpenAIEmbeddings()

        obj = cls(collection_name,embedding_function,persist_directory)

        if folder_path:
            files = [os.path.join(folder_path,f) for f in os.listdir(folder_path) if f.endswith(".pdf")]
            for file in files:
                obj.add_file(file)
        # obj.persist()
        return obj

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "sk-xxxx"
    os.environ["OPENAI_API_BASE"] = ""

    documents = chroma.get()
    n_documents = len(documents["ids"])
    for i in range(n_documents):
        text =documents["documents"][i].replace("\n","").replace(" ","")
        print(f"Document {i}: {documents['ids'][i]:<10s}...内容：{text[:20]:<20s}...{text[-20:]:<20s}")

    retriver = chroma.as_retriever()

