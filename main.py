from groq import Groq
import base64
import os
from load_dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "sf.png"

# Getting the base64 string
base64_image = encode_image(image_path)
def ask_groq(base64_image):
    chat_completion =client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "List what you observe in this photo in JSON format."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ]
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,)
    return json.loads(chat_completion.choices[0].message.content)

test=ask_groq(base64_image)
print(test)

#save the output in a json file
import json     
with open('output.json', 'w') as json_file:
    json.dump(test, json_file)



