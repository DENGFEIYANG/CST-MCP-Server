
from mcp.server.fastmcp import Context
import pycst
from utils.cst_session import get_cst

def register(mcp):
    @mcp.tool()
    def add_discrete_port(number: int, p1: list[float], p2: list[float]) -> str:
        """
        Adds a discrete port between two points.
        Args:
            number: Port number (e.g. 1)
            p1: [x, y, z] coordinates of point 1
            p2: [x, y, z] coordinates of point 2
        """
        mws = get_cst()
        try:
            pycst.discrete_port(mws, number, p1, p2)
            return f"Created discrete port {number} between {p1} and {p2}"
        except Exception as e:
            return f"Error creating port {number}: {str(e)}"

    @mcp.tool()
    def add_waveguide_port(number: int, 
                           xrange: list[float], yrange: list[float], zrange: list[float], 
                           orientation: str) -> str:
        """
        Adds a waveguide port.
        Args:
            number: Port number.
            xrange: [min, max]
            yrange: [min, max]
            zrange: [min, max]
            orientation: "xmin", "xmax", "ymin", "ymax", "zmin", "zmax"
        """
        mws = get_cst()
        try:
            # Defaulting extended ranges to 0 and coordinates to 'Free'
            pycst.waveguide_port(mws, number, xrange, yrange, zrange, 
                                 [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], 
                                 "Free", orientation)
            return f"Created waveguide port {number} at {orientation}"
        except Exception as e:
            return f"Error creating waveguide port {number}: {str(e)}"
