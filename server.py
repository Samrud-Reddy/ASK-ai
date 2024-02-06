import os
from flask import Flask, request
import llm
import vector_db
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin

app = Flask(__name__.split('.')[0])
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


load_dotenv()

pinecone_api = str(os.getenv("PINECONE_API_KEY"))
gemini = str(os.getenv("GEMINI_API_KEY"))

db = vector_db.Vector_database(gemini, pinecone_api)
model = llm.Llm(gemini, temp=0.8)


@app.route('/query', methods=["POST"])
@cross_origin()
def hello():
    if not request.is_json:
        return "Fail", 400

    # Access the JSON payload
    payload = request.json or {}
    subject = payload["subject"]
    question = payload["query"]

    paras = db.find_relevent_paras(question, subject, 5)
    
    ans = model.query(question, paras)
    print(ans)

    return ans


    


