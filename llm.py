import google.generativeai as genai

class Gemini:
    """
        A class creating a new Gemini model.
        Attributes:
            GEMINI_API_KEY (str): The Gemini Api Key
            model_name (str): The Name of the Model To Use
            safety settings (dict): The safety settings to obey
            temp (float): The temperature of the model
    """
    def __init__(self, GEMINI_API_KEY:str, model_name:str, safety_setting:dict=None, temp:float=1.0):
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(model_name=model_name, safety_settings=safety_setting, 
        generation_config=genai.types.GenerationConfig(
            temperature=temp
        ))
        self.model = model

    def start_chat(self):
        chat = self.model.start_chat(history=[])
        self.chat = chat
        return chat
    
    def send_chat_message(self, message:str, stream:bool=False):
        response = self.chat.send_message(content=message, stream=stream)
        return response
    
    def get_history(self):
        history = self.chat.history
        return history

def generate_prompt(question, relevant_paras):
    prompt = """Answer the question below with the data provided that you find relevant:
{question}
This is the data (in order of relevance):
para 1: {para_1}
para 2: {para_2}
para 3: {para_3}
para 4: {para_4}
para 5: {para_5}

Keep your answer a bit short where you can. Stay relevant to the question. 
""".format(question=question, para_1=relevant_paras[0], para_2=relevant_paras[1], para_3=relevant_paras[2], 
para_4=relevant_paras[3], para_5=relevant_paras[4])

    return prompt