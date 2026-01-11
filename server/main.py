
from mcp.server.fastmcp import FastMCP
import sys
import os

# Add parent directory to path so we can import 'utils' and 'tools'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import project, geometry, boolean, port, solver

# Initialize FastMCP
mcp = FastMCP("cst-studio-server")

# Register tools
print("Registering Project tools...", file=sys.stderr)
project.register(mcp)

print("Registering Geometry tools...", file=sys.stderr)
geometry.register(mcp)

print("Registering Boolean tools...", file=sys.stderr)
boolean.register(mcp)

print("Registering Port tools...", file=sys.stderr)
port.register(mcp)

print("Registering Solver tools...", file=sys.stderr)
solver.register(mcp)

if __name__ == "__main__":
    print("Starting Modular CST MCP Server...", file=sys.stderr)
    mcp.run()
