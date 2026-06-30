
from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6Jlq-HzesF-nSQHwXJINt09X70DwKKGCTuZrpqlCHrJlg"
)

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents="Product Volume shall be calculated as Product Length multiplied by Product Width multiplied by Product Height."
)

print(len(response.embeddings[0].values))

from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6Jlq-HzesF-nSQHwXJINt09X70DwKKGCTuZrpqlCHrJlg"
)

for model in client.models.list():
    print(model.name)