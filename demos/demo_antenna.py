
import asyncio
import sys
import os
import time

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_antenna_demo():
    server_script = os.path.join(os.path.dirname(__file__), "..", "server", "main.py")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
        env=os.environ.copy()
    )

    print(f"Connecting to server: {server_script}...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Create Project
            project_path = os.path.abspath("dipole_antenna.cst")
            print(f"\n[1] Creating project: {project_path}")
            res = await session.call_tool("create_project", arguments={"project_path": project_path})
            print(f"Result: {res.content[0].text}")

            print(f"\n[1.5] Setting Frequency Range")
            res = await session.call_tool("set_frequency_range", arguments={"min_freq": 4.0, "max_freq": 6.0})
            print(f"Result: {res.content[0].text}")

            # 2. Model Dipole
            print(f"\n[2] Setting Parameters")
            params = {"L_arm": 10.0, "Gap_half": 0.5, "Width": 1.0}
            res = await session.call_tool("set_parameters", arguments={"params": params, "rebuild": False})
            print(f"Result: {res.content[0].text}")

            print(f"\n[3] Creating Geometry (Bricks)")
            width = 1.0
            gap_half = 0.5
            l_arm = 10.0
            
            # Arm 1 (Top)
            res = await session.call_tool("add_brick", arguments={
                "name": "Arm1",
                "component": "Antenna",
                "material": "PEC",
                "xrange": [-width/2, width/2],
                "yrange": [-width/2, width/2],
                "zrange": [gap_half, gap_half + l_arm]
            })
            print(f"Result Arm1: {res.content[0].text}")

            # Arm 2 (Bottom)
            res = await session.call_tool("add_brick", arguments={
                "name": "Arm2",
                "component": "Antenna",
                "material": "PEC",
                "xrange": [-width/2, width/2],
                "yrange": [-width/2, width/2],
                "zrange": [-(gap_half + l_arm), -gap_half]
            })
            print(f"Result Arm2: {res.content[0].text}")

            print(f"\n[3.5] Adding Discrete Port")
            res = await session.call_tool("add_discrete_port", arguments={
                "number": 1,
                "p1": [0.0, 0.0, -0.5],
                "p2": [0.0, 0.0, 0.5]
            })
            print(f"Result Port: {res.content[0].text}")

            # 3. Solver
            print(f"\n[4] Running Solver (Mock/Real)")
            try:
                res = await session.call_tool("run_solver", arguments={"solver_type": "Time Domain"})
                print(f"Result Solver: {res.content[0].text}")
            except Exception as e:
                print(f"Solver failed (expected if license/setup issues): {e}")

            # 4. Export
            print(f"\n[5] Exporting Results")
            export_path = os.path.abspath("dipole_results.s1p")
            try:
                res = await session.call_tool("export_results", arguments={"export_path": export_path})
                print(f"Result Export: {res.content[0].text}")
            except Exception as e:
                print(f"Export failed: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_antenna_demo())
