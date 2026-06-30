# test_retrieval.py

from google import genai
from pinecone import Pinecone

GEMINI_API_KEY = "AQ.Ab8RN6Jlq-HzesF-nSQHwXJINt09X70DwKKGCTuZrpqlCHrJlg"
PINECONE_API_KEY = "pcsk_2wgQom_NwbC7kX8Vs4rb3KRERDZnvdYdhQ3P11DD4V3e14ofnTeng4tMfd78pWqEyW4tTR"

client = genai.Client(api_key=GEMINI_API_KEY)

pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index("business-rules")

query = """
product volume calculation
"""

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query
)

query_vector = response.embeddings[0].values

results = index.query(
    vector=query_vector,
    top_k=1,
    include_metadata=True
)

print(results)

for match in results.matches:

    print("\n")
    print("Rule ID :", match.id)
    print("Score   :", round(match.score,4))
    print("Rule    :", match.metadata["rule_text"])