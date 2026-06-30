from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key= "")

index_name = "business-rules"

existing = [idx["name"] for idx in pc.list_indexes()]

if index_name not in existing:
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

print("Index Ready")
