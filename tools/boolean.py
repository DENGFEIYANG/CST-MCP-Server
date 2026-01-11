
from mcp.server.fastmcp import Context
import pycst
from utils.cst_session import get_cst

def register(mcp):
    @mcp.tool()
    def boolean_add(target: str, tool: str) -> str:
        """Unions tool into target (Boolean Add)."""
        mws = get_cst()
        try:
            pycst.add(mws, target, tool)
            return f"Boolean Add: {target} + {tool}"
        except Exception as e:
            return f"Error Boolean Add: {str(e)}"

    @mcp.tool()
    def boolean_subtract(target: str, tool: str) -> str:
        """Subtracts tool from target (Boolean Subtract)."""
        mws = get_cst()
        try:
            pycst.subtract(mws, target, tool)
            return f"Boolean Subtract: {target} - {tool}"
        except Exception as e:
            return f"Error Boolean Subtract: {str(e)}"
            
    # Intersect was not found in pycst during inspection, we will try to use VBA directly or Solid.Intersect
    @mcp.tool()
    def boolean_intersect(target: str, tool: str) -> str:
        """Intersects target with tool."""
        mws = get_cst()
        try:
            # Try to invoke Solid.Intersect method via COM if pycst lacks it.
            # Solid object pattern:
            # s = mws.Solid
            # s.Intersect "target", "tool"
            
            s = mws.Solid
            s.Intersect(target, tool)
            return f"Boolean Intersect: {target} & {tool}"
        except Exception as e:
            return f"Error Boolean Intersect: {str(e)}"
