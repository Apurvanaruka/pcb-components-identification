import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

genai.configure(api_key="AIzaSyBpQKnPDPn4AQpQiCM4CzXz1ESXA8TDpxw")


def get_response(img, prompt = "Find out different compnent and give each component details in short. try to presize your response as much as possible do not give any other information also read text writen in the pcb and find out what type of cd it is" ):
    # sample_file_1 = PIL.Image.open(img)
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        response = model.generate_content([prompt, img]).text 
        return response
    except:
        return "You exceed todays tokens limit!"

