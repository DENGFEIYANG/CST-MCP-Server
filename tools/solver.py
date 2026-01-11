
from mcp.server.fastmcp import Context
import pycst
from utils.cst_session import get_cst

def register(mcp):
    @mcp.tool()
    def run_solver(solver_type: str = "Time Domain") -> str:
        """
        Runs the solver. Currently supports 'Time Domain'.
        """
        mws = get_cst()
        try:
            if solver_type.lower() == "time domain":
                # Assuming introspection showed: time_domain_solver(mws, steadyStateLimit)
                pycst.simulation.time_domain_solver(mws, -40) 
                return "Time Domain solver finished."
            else:
                return f"Solver type '{solver_type}' not implemented."
        except Exception as e:
            return f"Error running solver: {str(e)}"
