import vertexai
from vertexai import agent_engines

def test_live():
    # Initialize Vertex AI with target workspace project
    vertexai.init(project="agentspace-452714", location="us-central1")
    
    agent_engine_id = "9116920619588386816"

    print(f"Loading deployed agent: {agent_engine_id} ...")
    
    try:
         agent_engine = agent_engines.get(
              f"projects/agentspace-452714/locations/us-central1/reasoningEngines/{agent_engine_id}"
         )
         
         print("Agent retrieved successfully.")
         print(f"Display Name: {agent_engine.display_name}")
         print(f"Resource Name: {agent_engine.resource_name}")
         print(f"Creation Time: {agent_engine.create_time}")
         print("\nAgent is active and serving.")
         return

         
    except Exception as e:
         print(f"Error calling live agent: {e}")

if __name__ == "__main__":
    test_live()
