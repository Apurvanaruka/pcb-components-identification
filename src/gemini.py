import google.generativeai as genai
import PIL.Image
# from dotenv import load_dotenv
# import os

# load_dotenv()

# GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

# print(GOOGLE_API_KEY)
genai.configure(api_key="AIzaSyAwIEpg7iGKz-LoYdRBnoF1hycvT5Ks77U")

def get_response(img, prompt = "Find out different compnent and give each component details in short. try to presize your response as much as possible do not give any other information" ):
    sample_file_1 = PIL.Image.open('../dataset/train/images/VID20210601144014-45_jpg.rf.1fc301cb2464b72cbf29ddae321791c3.jpg')
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        return model.generate_content([prompt, sample_file_1]).text
    except e:
        return "You exceed todays tokens limit!"

