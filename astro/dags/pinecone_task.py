from google import genai
from pinecone import Pinecone

GEMINI_API_KEY = "AQ.Ab8RN6Jlq-HzesF-nSQHwXJINt09X70DwKKGCTuZrpqlCHrJlg"
PINECONE_API_KEY = "pcsk_2wgQom_NwbC7kX8Vs4rb3KRERDZnvdYdhQ3P11DD4V3e14ofnTeng4tMfd78pWqEyW4tTR"

client = genai.Client(api_key=GEMINI_API_KEY)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("business-rules")


def pinecone_task(rule_description):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=rule_description
    )

    query_vector = response.embeddings[0].values

    results = index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True
    )

    rules = ""

    for match in results.matches:

        rules += match.metadata["rule_text"]

        rules += "\n\n"

    return rules