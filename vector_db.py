from multiprocessing import Pool
from converter import Paragraph
import pinecone
import time
import google.generativeai as genai


class Vector_database:
    """An class representing a Vector_database 
        Attributes:
            GEMINI_API_KEY (str): The api key for Gemini
            PINECONE_API_KEY (str): The api key for Pinceone
            environment (str): The environment name for pinecone
            index (idk): The pinecone Index
    """
    def __init__(self, GEMINI_API_KEY, PINECONE_API_KEY, environment = "gcp-starter"):
        self.GEMINI_API_KEY = GEMINI_API_KEY
        self.PINECONE_API_KEY = PINECONE_API_KEY
        self.environment = environment


        genai.configure(api_key=GEMINI_API_KEY)
        pinecone.init(api_key=PINECONE_API_KEY, environment="gcp-starter")

        self.index = pinecone.Index("textbooks")

    def get_embedings_for_retrival_query(self, text: str) -> list[float]:
        """Gets vector embedings for a retrieval_query
            Attributes:
                text (str): The text to get embedings for retrieval query

            RETURNS a 768 dimensional array of floats
        """
        return genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_query",
        )["embedding"]

    def get_embedings_for_indexing(self, text: str, title: str) -> list[float]:
        """Gets vector embedings for a document to retrieval
            Attributes:
                text (str): The text to get embedings for retrieval query
                title (str): The title of the document to embedd

            RETURNS a 768 dimensional array of floats
        """
        return genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document",
            title=title,
        )["embedding"]

    def create_vector(self, para: Paragraph):
        """Creates vectors that can be passed into upsert
            Attributes:
                para (converter.Paragraph): A Paragraph object from converter

            RETURN a tuple with (id(str), embeding(list[floats]), metadata[dict])
        """
        id = str(para.textbook_name)+"&"+str(para.page)+"&"+str(para.chapter_name)+"&"+str(para.para_no)+"&"+str(para.height)
        embeds = self.get_embedings_for_indexing(para.text, para.textbook_name)
        metadata = {
                "lines":para.lines,
                "textbook_name":para.textbook_name,
                "subject_name":para.subject_name,
                "page":para.page,
                "para_no":para.para_no,
                "height":para.height,
                "chapter":str(para.chapter_name)
                }
        return (id, embeds, metadata)

    def add_paragraphs(self, paras: list[Paragraph]) -> None:
        """Adds paragraphs to the vector database
            Attributes:
                paras (converter.Paragraph): A paragraph object from converter
        """

        namespace = paras[0].subject_name

        def divide_chunks(array, chunk_size): 
            # looping till length l 
            for i in range(0, len(array), chunk_size):  
                yield array[i:i + chunk_size] 
        
        vectors = list(map(self.create_vector, paras))

        for chunk in divide_chunks(vectors, 80):
            self.index.upsert(vectors=chunk, namespace = namespace)
            # time.sleep(1000)

        
    def index_return_to_Paragraph(self, item) -> Paragraph:
        """Converts the item returned by index to a Paragraph
            Attributes:
                item (NA): The item returned by the vectorsearch
        """
        lines = [line.split(" ") for line in item["metadata"]["lines"]]
        return Paragraph(lines, item["metadata"]["textbook_name"], item["metadata"]["page"], item["metadata"]["para_no"], item["metadata"]["height"], item["metadata"]["chapter"])
    

    def find_relevent_paras(self, query: str, subject_name: str|None = None, no_results: int = 3) -> list[Paragraph]:
        query_vector = self.get_embedings_for_retrival_query(query)

        if subject_name:
            results = self.index.query(vector=query_vector, top_k=no_results, include_metadata=True, namespace=subject_name)
        else:
            results = self.index.query(vector=query_vector, top_k=no_results, include_metadata=True)

        results = results["matches"]
        results = list(map(self.index_return_to_Paragraph, results))

        return results

