import converter
import google.generativeai as genai
import pinecone
import multiprocessing


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

        self.index = pinecone.Index("textbooks")

        genai.configure(api_key=GEMINI_API_KEY)
        pinecone.init(api_key=PINECONE_API_KEY, environment="gcp-starter")

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

    def create_vector(self, para: converter.Paragraph):
        """Creates vectors that can be passed into upsert
            Attributes:
                para (converter.Paragraph): A Paragraph object from converter

            RETURN a tuple with (id(str), embeding(list[floats]), metadata[dict])
        """
        id = str(para.textbook_name)+"&"+str(para.page)+"&"+str(para.chapter_name)+"&"+str(para.para_no)+"&"+str(para.height)
        print("sending "+id)
        embeds = self.get_embedings_for_indexing(para.text, para.textbook_name)
        metadata = {
                "text": para.text,
                "textbook_name": para.textbook_name,
                "chapter_name": para.chapter_name,
                "page_no": para.page,
                }
        return (id, embeds, metadata)

    def add_paragraphs(self, paras: list[converter.Paragraph]) -> None:
        namespace = paras[0].textbook_name

        def divide_chunks(array, chunk_size): 
            # looping till length l 
            for i in range(0, len(array), chunk_size):  
                yield array[i:i + chunk_size] 
        
        with multiprocessing.Pool(20) as p:
            vectors = p.map(self.create_vector, paras)


        for chunk in divide_chunks(vectors, 100):
            self.index.upsert(vectors=chunk, namespace = namespace)
        
