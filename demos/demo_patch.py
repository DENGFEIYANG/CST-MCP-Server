
import asyncio
import sys
import os
import time

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_patch_demo():
    # Adjust path to server/main.py
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
            
            project_path = os.path.abspath("patch_microstrip.cst")
            print(f"\n[1] Creating project: {project_path}")
            await session.call_tool("create_project", arguments={"project_path": project_path})
            
            print(f"\n[2] Setting Frequency")
            await session.call_tool("set_frequency_range", arguments={"min_freq": 2.0, "max_freq": 4.0})

            # Dimensions
            sub_w, sub_l = 60.0, 60.0
            sub_h = 1.6
            patch_w, patch_l = 40.0, 30.0
            feed_w = 3.0 # Approx 50 ohm
            feed_len = (sub_l/2) - (patch_l/2) # 15mm
            
            print(f"\n[3] Creating Substrate (Vacuum/Dielectric)")
            # 60x60x1.6 mm. Center 0,0.
            await session.call_tool("add_brick", arguments={
                "name": "Substrate",
                "component": "Substrate",
                "material": "Vacuum", 
                "xrange": [-sub_w/2, sub_w/2],
                "yrange": [-sub_l/2, sub_l/2],
                "zrange": [0.0, sub_h]
            })

            print(f"\n[3.5] Creating Ground (PEC)")
            # Bottom face z=0. Thickness 0.035
            await session.call_tool("add_brick", arguments={
                "name": "Ground",
                "component": "Antenna",
                "material": "PEC", 
                "xrange": [-sub_w/2, sub_w/2],
                "yrange": [-sub_l/2, sub_l/2],
                "zrange": [-0.035, 0.0]
            })

            print(f"\n[4] Creating Patch (PEC)")
            # On top z=sub_h.
            await session.call_tool("add_brick", arguments={
                "name": "Patch",
                "component": "Antenna",
                "material": "PEC",
                "xrange": [-patch_w/2, patch_w/2],
                "yrange": [-patch_l/2, patch_l/2],
                "zrange": [sub_h, sub_h+0.035]
            })
            
            print(f"\n[5] Creating Microstrip Feed (PEC)")
            # Connects from edge (y=-30) to patch (y=-15).
            # Width=3. Xrange=[-1.5, 1.5]
            feed_start_y = -sub_l/2
            feed_end_y = -patch_l/2
            
            await session.call_tool("add_brick", arguments={
                "name": "Feed",
                "component": "Antenna",
                "material": "PEC",
                "xrange": [-feed_w/2, feed_w/2],
                "yrange": [feed_start_y, feed_end_y],
                "zrange": [sub_h, sub_h+0.035]
            })

            print(f"\n[6] Boolean Union: Patch + Feed")
            # Target: "Antenna:Patch"
            # Tool: "Antenna:Feed"
            res = await session.call_tool("boolean_add", arguments={
                "target": "Antenna:Patch",
                "tool": "Antenna:Feed"
            })
            print(f"Result Boolean: {res.content[0].text}")
            
            print(f"\n[7] Adding Waveguide Port")
            # At Y = -30 (ymin).
            # Xrange [-15, 15]
            res = await session.call_tool("add_waveguide_port", arguments={
                "number": 1,
                "xrange": [-15.0, 15.0],
                "yrange": [feed_start_y, feed_start_y],  # Flat on face
                "zrange": [0.0, 8.0],
                "orientation": "ymin"
            })
            print(f"Result Port: {res.content[0].text}")

            print(f"\n[8] Solving")
            try:
                res = await session.call_tool("run_solver", arguments={"solver_type": "Time Domain"})
                print(f"Result Solver: {res.content[0].text}")
            except Exception as e:
                print(f"Solver issue: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_patch_demo())
