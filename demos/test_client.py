
import asyncio
import sys
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_client():
    server_script = os.path.join(os.path.dirname(__file__), "..", "server", "main.py")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
        env=os.environ.copy() 
    )

    print(f"Connecting to server: {server_script}")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. List tools
            print("\n--- Initializing & Listing Tools ---")
            await session.initialize()
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            print("\n--- Server is ready and tools are exposed ---")
            
            # Test create_project
            project_path = os.path.abspath("test_project.cst")
            print(f"\n--- Calling create_project({project_path}) ---")
            try:
                result = await session.call_tool("create_project", arguments={"project_path": project_path})
                print(f"Result: {result.content}")
            except Exception as e:
                print(f"Tool execution failed: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        asyncio.run(run_client())
    except Exception as e:
        print(f"Error: {e}")
