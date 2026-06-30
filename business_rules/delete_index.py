from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_2wgQom_NwbC7kX8Vs4rb3KRERDZnvdYdhQ3P11DD4V3e14ofnTeng4tMfd78pWqEyW4tTR")

pc.delete_index("business-rules")

print("Deleted")