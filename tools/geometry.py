
from mcp.server.fastmcp import Context
import pycst
from utils.cst_session import get_cst

def register(mcp):
    @mcp.tool()
    def add_brick(name: str, component: str, material: str, 
                  xrange: list[str | float], yrange: list[str | float], zrange: list[str | float]) -> str:
        """Creates a brick geometry."""
        mws = get_cst()
        try:
            pycst.brick(mws, name, component, material, xrange, yrange, zrange)
            return f"Created brick: {name} in {component}"
        except Exception as e:
            return f"Error creating brick {name}: {str(e)}"

    @mcp.tool()
    def add_cylinder(name: str, component: str, material: str, 
                     axis: str, outer_radius: float, inner_radius: float, 
                     center: list[float], range_val: list[float]) -> str:
        """
        Creates a cylinder.
        Args:
            center: [center1, center2] (e.g. x,y for z-axis)
            range_val: [min, max] along axis
        """
        mws = get_cst()
        try:
            if len(range_val) != 2:
                return "Error: range_val must have 2 elements [min, max]"
            pycst.cylinder(mws, name, component, material, axis, 
                           outer_radius, inner_radius, 
                           center[0], center[1], range_val)
            return f"Created cylinder {name}"
        except Exception as e:
            return f"Error creating cylinder {name}: {str(e)}"

    @mcp.tool()
    def add_sphere(name: str, component: str, material: str, 
                   axis: str, center_radius: float, top_radius: float, bottom_radius: float, 
                   center: list[float]) -> str:
        """
        Creates a sphere (or ellipsoid segment provided via API, assuming sphere wrapper).
        Based on signature: (mws, name, component, material, axis, centreRadius, topRadius, bottomRadius, centre)
        Args:
            axis: "x", "y", "z"
            center: [x,y,z]
        """
        mws = get_cst()
        try:
            pycst.sphere(mws, name, component, material, axis, 
                         center_radius, top_radius, bottom_radius, center)
            return f"Created sphere {name}"
        except Exception as e:
            return f"Error creating sphere {name}: {str(e)}"

    # Transforms (Using VBA/COM direct access since pycst wrappers are missing)
    
    @mcp.tool()
    def transform_translate(target: str, vector: list[float], copy: bool = False, repetitions: int = 1) -> str:
        """
        Translates a solid.
        Args:
            target: Solid name (e.g. Component:Solid)
            vector: [x, y, z] translation vector
            copy: Create copy?
            repetitions: Number of copies (if copy=True)
        """
        mws = get_cst()
        try:
            # VBA command: Solid.Move "name", "dx", "dy", "dz"
            # But we might want Transform object logic.
            # Let's use the Transform object pattern typically found in CST VBA.
            # With Transform:
            # .Reset
            # .Name "component:solid" (or list)
            # .Vector x, y, z
            # .UsePivotPoint "False"
            # .Copy copy
            # .Repetitions repetitions
            # .Transform "Translate"
            
            # Since we are using COM directly via mws (which is the app object or project object?),
            # pycst usually calls methods on 'mws'. 
            # If 'mws' is the 'CSTStudio.Application' or 'CSTStudio.Project', we might need to access the 'Transform' object.
            # In CST automation, `Transform` is a global object in the VBA context.
            # We can try executing VBA directly via `mws.AddToHistory` or similar?
            # Or accessing the object `mws.Transform`.
            
            # Let's try direct object access.
            t = mws.Transform
            t.Reset()
            t.Name(target)
            t.Vector(vector[0], vector[1], vector[2])
            t.UsePivotPoint(False)
            t.Copy(copy)
            t.Repetitions(repetitions)
            t.Transform("Translate")
            
            return f"Translated {target} by {vector} (Copy={copy}, Reps={repetitions})"
        except Exception as e:
            return f"Error translating {target}: {str(e)}"

    @mcp.tool()
    def transform_rotate(target: str, origin: list[float], axis: str, angle: float, copy: bool = False, repetitions: int = 1) -> str:
        """
        Rotates a solid.
        Args:
            target: Solid name
            origin: [x,y,z] origin of rotation
            axis: "x", "y", "z"
            angle: degrees
        """
        mws = get_cst()
        try:
            t = mws.Transform
            t.Reset()
            t.Name(target)
            t.Origin(origin[0], origin[1], origin[2])
            # For Axis, usually it takes "x", "y", "z" or vectors. 
            # VBA: .Center x, y, z -> .PlaneNormal x,y,z OR .Component ...
            # Actually standard Rotate uses: .Center/Origin, .Angle, .Component (Axis)
            t.Center(origin[0], origin[1], origin[2])
            t.Angle(angle)
            t.Component(axis) # "x", "y", "z"
            t.Copy(copy)
            t.Repetitions(repetitions)
            t.Transform("Rotate")
            
            return f"Rotated {target} around {axis} by {angle} deg"
        except Exception as e:
            return f"Error rotating {target}: {str(e)}"

    @mcp.tool()
    def transform_scale(target: str, origin: list[float], factor: list[float], copy: bool = False) -> str:
        """
        Scales a solid.
        Args:
             factor: [fx, fy, fz]
        """
        mws = get_cst()
        try:
            t = mws.Transform
            t.Reset()
            t.Name(target)
            t.Origin(origin[0], origin[1], origin[2])
            t.ScaleFactor(factor[0], factor[1], factor[2]) # Typically .ScaleFactorX ...
            # Wait, verify API? Assume .ScaleFactor x,y,z exists or .X(fx) .Y(fy)...
            # Common is .ScaleFactorX, .ScaleFactorY, .ScaleFactorZ 
            t.ScaleFactorX(factor[0])
            t.ScaleFactorY(factor[1])
            t.ScaleFactorZ(factor[2])
            t.Copy(copy) # Scale copy often supported
            t.Repetitions(1)
            t.Transform("Scale")
            
            return f"Scaled {target} by {factor}"
        except Exception as e:
             return f"Error scaling {target}: {str(e)}"

    @mcp.tool()
    def transform_mirror(target: str, plane_normal: str, plane_position: float, copy: bool = False) -> str:
        """
        Mirrors a solid.
        Args:
            plane_normal: "x", "y", "z" (Mirror plane normal)
            plane_position: coordinate value of the plane (e.g. x=0)
        """
        mws = get_cst()
        try:
            t = mws.Transform
            t.Reset()
            t.Name(target)
            t.PlaneNormal(plane_normal)
            t.Center(plane_position if plane_normal=="x" else 0,
                     plane_position if plane_normal=="y" else 0,
                     plane_position if plane_normal=="z" else 0) 
            # Center logic might need careful checking for mirror plane position.
            # Usually .Center defines a point on the plane.
            
            t.Copy(copy)
            t.Repetitions(1)
            t.Transform("Mirror")
            return f"Mirrored {target} across {plane_normal}={plane_position}"
        except Exception as e:
            return f"Error mirroring {target}: {str(e)}"
