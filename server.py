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


def convert(history):
    is_user = True
    out = []
    for msg in history:
        part = {
            "parts": {
                "text": msg
            },
            "role": "user" if is_user else "model"
        }
        is_user = not is_user
        out.append(part)
    
    return out



@app.route('/query', methods=["POST"])
@cross_origin()
def query():

    if not request.is_json:
        return "Failed cause value is not JSON", 400

    # Access the JSON payload
    payload = request.json or {}
    subject = payload["subject"]
    question = payload["query"]
    history = payload["history"]
    new_hist = convert(history=history)
    model = llm.Llm(gemini, temp=0.8, history=new_hist)

    if subject is None or question is None or history is None:
        return "Failed because you forgot to pass in something", 400

    subject_translate = {"Chemistry": "chem"}


    if subject in subject_translate:
        paras = db.find_relevent_paras(question, subject_translate[subject], 5)
        ans = model.query(question, paras)

        print(paras)
        print("Response is " + ans)

        return ans
    else:
        return "FAILED cause subject is wrong", 400


    


