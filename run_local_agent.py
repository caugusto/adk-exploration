import asyncio
import os
import sys
import vertexai

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

vertexai.init(project="agentspace-452714", location="us-central1")

import agent
root_agent = agent.root_agent

async def main():
    print("--- Executing Local Agent `run_async` ---")
    try:
        responses = []
        # Using positional argument or input=
        # Standard ADK signature often uses positionals or kwargs inspection
        async for event in root_agent.run_async("Hi, call test_tool first"):
            print(f"EVENT: {event}")
            responses.append(event)
        
        print("\n--- Final Output ---")
        for r in responses:
             print(r)
             
    except Exception as e:
         import traceback
         traceback.print_exc()
         print(f"Local execution crashed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
