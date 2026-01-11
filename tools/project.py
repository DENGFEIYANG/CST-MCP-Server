
from mcp.server.fastmcp import Context
import pycst
import os
import sys
from utils.cst_session import get_cst

def register(mcp):
    @mcp.tool()
    def open_project(project_path: str = None) -> str:
        """
        Opens an existing CST project or creates a new one.
        If project_path is None, opens a new project.
        """
        mws = get_cst()
        if project_path:
            if os.path.exists(project_path):
                 try:
                     mws.OpenFile(project_path)
                     return f"Opened project: {project_path}"
                 except Exception as e:
                     return f"Error opening project: {str(e)}"
            else:
                 return f"Project path {project_path} not found. Using current active project."
        return "Using current active project."

    @mcp.tool()
    def create_project(project_path: str) -> str:
        """
        Creates a new CST project and saves it to the specified path.
        Args:
            project_path: Full path to save the new project (e.g. "C:\\Temp\\test.cst")
        """
        mws = get_cst()
        try:
            pycst.save_as_project(mws, project_path)
            return f"Created and saved new project at: {project_path}"
        except Exception as e:
            return f"Error creating project: {str(e)}"

    @mcp.tool()
    def save_project() -> str:
        """Saves the current project."""
        mws = get_cst()
        try:
            pycst.save_project(mws)
            return "Project saved."
        except Exception as e:
            return f"Error saving project: {str(e)}"

    @mcp.tool()
    def save_as_project(project_path: str) -> str:
        """Saves the current project to a new path."""
        mws = get_cst()
        try:
            pycst.save_as_project(mws, project_path)
            return f"Project saved as: {project_path}"
        except Exception as e:
            return f"Error saving project as: {str(e)}"

    @mcp.tool()
    def set_parameters(params: dict[str, float], rebuild: bool = True) -> str:
        """
        Sets one or more parameters in the CST project.
        Args:
            params: dictionary of parameter names and values.
            rebuild: whether to trigger a geometry rebuild (default True).
        """
        mws = get_cst()
        results = []
        try:
            print(f"Setting parameters: {params.keys()}", file=sys.stderr)
            for name, value in params.items():
                mws.StoreParameter(name, value)
                results.append(f"{name}={value}")
            
            if rebuild:
                print("Rebuilding geometry...", file=sys.stderr)
                mws.RebuildOnParametricChange(False, False)
                return f"Set parameters: {', '.join(results)} and rebuilt geometry."
            else:
                return f"Set parameters: {', '.join(results)} (no rebuild)."
        except Exception as e:
            print(f"Error in set_parameters: {e}", file=sys.stderr)
            return f"Error setting parameters: {str(e)}"

    @mcp.tool()
    def set_frequency_range(min_freq: float, max_freq: float) -> str:
        """
        Sets the frequency range of the project.
        """
        mws = get_cst()
        try:
            pycst.frequency_range(mws, min_freq, max_freq)
            return f"Set frequency range: {min_freq} - {max_freq}"
        except Exception as e:
            return f"Error setting frequency range: {str(e)}"

    @mcp.tool()
    def export_results(export_path: str) -> str:
        """
        Exports S-parameters to a Touchstone file.
        """
        mws = get_cst()
        try:
            pycst.export_touchstone(mws, export_path)
            return f"Exported Touchstone to {export_path}"
        except Exception as e:
            return f"Error exporting results: {str(e)}"
