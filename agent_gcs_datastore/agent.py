import os
import dotenv

# GCS Search Imports
from google.cloud import discoveryengine_v1 as discoveryengine
from google.api_core.client_options import ClientOptions

# ADK Imports
from google.adk.agents import Agent
from google.genai import types

dotenv.load_dotenv()

# --- CONFIGURATION ---
PROJECT_ID = "<CHANGE-ME>"

# Datastore / Discovery Engine Configuration
ENGINE_ID = "<CHANGE-ME>" ## Gemini Enterprise App ID
DATA_STORE_ID = "<CHANGE-ME>" ## Vertex Search Data Store ID
DATASTORE_LOCATION = "global" ## Datastore location. Other values include us, etc

# Model Configuration
#MODEL_NAME = "gemini-2.5-flash"
#MODEL_NAME = "gemini-2.5-flash-lite-preview-09-2025"
#MODEL_NAME = "gemini-3-flash-preview"
MODEL_NAME = "gemini-3.1-pro-preview"

# --- CUSTOM TOOLS ---

def search_gcs_documents(query: str) -> str:
    """
    Searches the GCS Document Data Store for catalogs, drawings, and technical specifications,
    and returns the raw search snippets and links for the agent to analyze.
    """
    # --- STEP 1: Search Discovery Engine ---
    client_options = (
        ClientOptions(api_endpoint=f"{DATASTORE_LOCATION}-discoveryengine.googleapis.com")
        if DATASTORE_LOCATION != "global" else None
    )
    client = discoveryengine.SearchServiceClient(client_options=client_options)
    
    ds_spec = discoveryengine.SearchRequest.DataStoreSpec(
        data_store=f"projects/{PROJECT_ID}/locations/{DATASTORE_LOCATION}/collections/default_collection/dataStores/{DATA_STORE_ID}"
    )
    
    request = discoveryengine.SearchRequest(
        serving_config=f"projects/{PROJECT_ID}/locations/{DATASTORE_LOCATION}/collections/default_collection/engines/{ENGINE_ID}/servingConfigs/default_search",
        query=query,
        page_size=5,
        content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
            snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
                return_snippet=True,
            ),
        ),
        data_store_specs=[ds_spec]
    )

    print(f"\n[Executing GCS Search]: Searching GCS Store for: '{query}'...")
    try:
        response = client.search(request=request)
    except Exception as e:
        return f"Error executing search against data store: {str(e)}"

    # --- STEP 2: Extract & Convert Links ---
    context_text = ""
    print(f"Found {len(response.results)} documents. Preparing context...")
    
    for i, result in enumerate(response.results, 1):
        data = result.document.derived_struct_data
        title = data.get("title", f"Document {i}")
        
        # Link conversion: gs:// -> https://storage.cloud.google.com/
        raw_link = data.get("link", "")
        formatted_link = raw_link.replace("gs://", "https://storage.cloud.google.com/", 1)
            
        if "snippets" in data and len(data["snippets"]) > 0:
            snippet = data["snippets"][0].get("snippet", "").replace("\n", " ")
            context_text += f"SOURCE {i}: {title}\nLINK: {formatted_link}\nTEXT: {snippet}\n\n"

    if not context_text:
        print("⚠️ No relevant documents found.")
        return "No relevant documents found in the GCS catalog for this query."

    return context_text

# --- PROMPT CONSTRUCTION ---

def build_system_instruction():
    """
    Constructs the dynamic system prompt tailored strictly for Document Retrieval.
    """
    
    return """
# Document & Drawing Retrieval Agent Instructions

You are a specialized expert for retrieving technical files, drawings, and catalog information for Switchcraft/Conxall products.

## 1. Intent & Tool Usage
* Analyze every user input to identify the document or drawing they are looking for.
* **`search_gcs_documents`**: You MUST use this tool IMMEDIATELY to search for documents, drawings, and catalog data. Pass the user's search query (e.g., "catalog for PT8FX8MX2DB25") directly to this tool.

## 2. Document Retrieval Protocol
1. **Tool Execution:** Use ONLY the `search_gcs_documents` tool to query the GCS Vertex AI Search datastore.
2. **Analysis & Response:** The tool returns raw text snippets and document links. Read the provided snippets carefully and extract technical details (materials, dimensions, specs) to answer the user's question accurately.
3. **Citation (MANDATORY):** Use clickable Markdown links for inline citations using the format `[[Source X]](URL)` for every fact mentioned (do not display the raw URL inline). 
4. **References List:** At the end of your response, create a "## References" section listing every source used in the format: `[Source X]: Document Title - URL`.
5. **Final Action:** After providing the document details and links, politely ask if the user has any other questions. Do not offer an email draft.

## 3. Output Format & Branding
* **Source Citation:** Always end your response with: 
  > **Source:** search_gcs_documents
"""

# --- AGENT INITIALIZATION ---

# 1. Build the instruction block
system_instruction_payload = build_system_instruction()

# 2. Define the ADK Agent
root_agent = Agent(
    model=MODEL_NAME,
    name="document_retrieval_agent",
    description="Specialized agent for retrieving technical files, drawings, and catalog information via GCS Search.",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
        top_p=0.1,
        # This is the standard way to pass timeouts to the underlying Vertex AI/Gemini SDK
        # 60000 milliseconds = 60 seconds
        http_options={"timeout": 60000}
        # Note: The original file didn't have retry logic here, but you can add it if needed:
        # retry=google.api_core.retry.Retry()
    ),
    # Disabled BuiltInPlanner to prevent context overloading/hanging
    instruction=system_instruction_payload,
    tools=[search_gcs_documents]
)

# def get_root_agent():
#     """Returns the initialized ADK Root Agent"""
#     return root_agent

# if __name__ == "__main__":
#     # Test block to verify agent loads successfully 
#     agent = get_root_agent()
#     print("\n--- ADK Agent Initialized ---")
#     print(f"Agent Name: {agent.name}")
#     print(f"Model: {agent.model}")
#     print("Agent is ready to be executed via ADK orchestrator.")
