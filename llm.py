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
        print(history)
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

    def query(self, question, paras, history) -> str:
        prompt = self.generate_prompt(question, paras, history=history)
        return str(self.send_chat_message(prompt).text)

    @staticmethod
    def generate_prompt(question, relevant_paras, history):
        prompt = f"""Answer the question.
    {question}
    This is the data (in order of relevance):\n
    """ 
        if relevant_paras:
            for (i, paras) in enumerate(relevant_paras):
                prompt += f"para {i}: {paras}\n"
        else:
            prompt += "There is no relevant data, try using your own knowledge\n"

        prompt += "Keep your answer a bit short where you can. Stay relevant to the question.\n"
        prompt += "The history of this chat is: \n"
        if history:
            for (i, msg) in enumerate(history):
                if i % 2 == 0:
                    prompt += f"User: {msg}\n"
                else:
                    prompt += f"AI: {msg}\n"

        return prompt
