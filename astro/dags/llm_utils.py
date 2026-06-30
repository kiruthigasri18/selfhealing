import time
from google import genai

GEMINI_API_KEY = "AQ.Ab8RN6Jlq-HzesF-nSQHwXJINt09X70DwKKGCTuZrpqlCHrJlg"

client = genai.Client(api_key=GEMINI_API_KEY)

MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-2.0-flash",
]


def llm_call(prompt):

    for model in MODELS:

        for retry in range(3):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                return response.text

            except Exception as e:

                print(
                    f"{model} failed attempt {retry+1}:",
                    e
                )

                time.sleep(10)

    raise Exception("All models failed")