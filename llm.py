import google.generativeai as genai
import google.generativeai.protos as prot
import os
from dotenv import load_dotenv

class LLM():
    def __init__(self):
        load_dotenv()
        genai.configure(api_key = os.getenv("GENAI_API_KEY"))   
        
        self.model = genai.GenerativeModel(
            'gemini-1.5-flash-latest',
            generation_config = genai.GenerationConfig(
                temperature = 0.7
            ),
            system_instruction = ["""
                Eres un chef profesional experto en cocina internacional llamado Cookly. 
                Tu objetivo es proporcionar recetas elaboradas claras y detalladas según las indicaciones que se te den.
                También puedes proporcionar información relevante y responder preguntas o dar consejos.
                Si es que los ingredientes se pueden comprar, brinda una opción que cuente con los ingredientes que te pide y complementalos con los ingredientes que se pueden comprar para generar una receta aceptable 
                Si la indicación es poco clara y no tiene que ver con recetas, debes responder con un mensaje de error o aclarar que solo aconsejas sobre recetas.
                Al momento de entregar las recetas responde siempre en el siguiente formato Markdown estructurado:
                **[Nombre del platillo]**

                **Ingredientes**

                - [Ingrediente 1]
                - [Ingrediente 2]
                - [...]

                **Proceso de cocina**

                1. [Paso 1]
                2. [Paso 2]
                3. [...]

                **Información Nutricional**

                - [Calorías por porción]
                - [Otro dato nutricional, si aplica]

                **Consejo nutricional**

                [Consejo sobre los beneficios de algún ingrediente]

                **Consejo culinario**

                [Sugerencia para mejorar el sabor, presentación o versatilidad del platillo]
            """]
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=False)

    def generate_response(self, prompt, portions):
        dishes = self.load_dishes()
        
        if not dishes:
            return "No se encontraron platillos disponibles en la lista. Por favor, utiliza la version libre."
        
        dishes_str = "\n- ".join(dishes)
        
        prompt = f"""
        {prompt} El número de porciones es {portions}. Solo puedes elaborar recetas de la lista o basadas en la lista, si no puedes elaborar alguna, lo indicas y muestras una adaptación de alguna de las recetas de la lista.
        Responde en el formato que se te indicó. La lista de recetas que puedes elaborar es la siguiente:
        - {dishes_str}
        """
        print(prompt)
        
        response = self.chat.send_message(prompt) #candidate_count=1
        message= response.candidates[0].content.parts[0].text
        
        print(message)
        return message
    
    def generate_free_response(self, prompt, portions):
        prompt = f"Puedes elaborar cualquier platillo del mundo o adaptarlo según la solicitud. El número de porciones es {portions}. Responde en el formato que se te indico."
        print(prompt)
        response = self.chat.send_message(prompt) #candidate_count=1
        message= response.candidates[0].content.parts[0].text
        print(message)
        return message


    def load_dishes(self):
        dishes_list = []
        try:
            with open(os.path.join("static", "dishes.txt"), "r") as file:
                dishes_list = file.read().splitlines()  # Leer cada línea del archivo y almacenarla en una lista
        except FileNotFoundError:
            print("El archivo dishes.txt no se encuentra.")
        return dishes_list