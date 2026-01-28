
import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings

# Load env
load_dotenv(override=True)

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")

print(f"Testing Azure Embedding with:")
print(f"Endpoint: {endpoint}")
print(f"Deployment: {deployment}")
print(f"Version: {api_version}")

try_deployments = [
    os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    "text-embedding-ada-002",
    "embedding",
    "embeddings",
    "text-embedding",
    "ada-002",
    "ada",
    "gpt-4-embedding" 
]

# Remove duplicates and None
try_deployments = list(set([d for d in try_deployments if d]))

print(f"Testing deployments: {try_deployments}")

for dep in try_deployments:
    print(f"\n--- Testing deployment: '{dep}' ---")
    try:
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=dep,
            openai_api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key
        )
        
        text = "This is a test"
        query_result = embeddings.embed_query(text)
        print(f"SUCCESS! Found valid deployment: '{dep}'")
        break
    except Exception as e:
        if "DeploymentNotFound" in str(e):
             print(f"Failed: Deployment not found")
        else:
             print(f"ERROR: {e}")
