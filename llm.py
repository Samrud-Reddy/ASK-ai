import google.generativeai as genai

class Llm:
    """
        A class creating a new Gemini model.
        Attributes:
            GEMINI_API_KEY (str): The Gemini Api Key
            model_name (str): The Name of the Model To Use
            safety settings (dict): The safety settings to obey
            temp (float): The temperature of the model
    """
    def __init__(self, GEMINI_API_KEY:str, model_name:str="models/gemini-pro", safety_setting=None, temp:float=1.0, history=[]):
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(model_name=model_name, safety_settings=safety_setting, 
        generation_config=genai.types.GenerationConfig(
            temperature=temp
        ))
        self.model = model
        self.start_chat(hist=history)

    def start_chat(self, hist):
        chat = self.model.start_chat(history=hist)
        self.chat = chat
        return chat
    
    def send_chat_message(self, message:str, stream:bool=False):
        response = self.chat.send_message(content=message, stream=stream)
        return response
    
    def get_history(self):
        history = self.chat.history
        return history

    def query(self, question, paras) -> str:
        prompt = self.generate_prompt(question, paras)
        return str(self.send_chat_message(prompt).text)

    @staticmethod
    def generate_prompt(question, relevant_paras):
        prompt = f"""Answer the question below using the data provided and your own knowledge if the data is insufficient.
        Also, the user may ask a question using their chat history, such as "But why is this?" when their previous question
        asked for the reactions between acid and base, for example. In this case, when you feel it is suitable, ignore the
        data provided, as it may not be too relevant (given the data doesn't know the previous context of the chat), and reply
        normally.
    {question}
    This is the data (in order of relevance):
    """ 
            
        for (i, paras) in enumerate(relevant_paras):
            prompt += f"para {i}: {paras}"

        prompt += "Keep your answer a bit short where you can. Stay relevant to the question."

        return prompt
