import FreeCAD as App
import Part

from metal_primitives.app.feature_base import FeatureBase
from metal_primitives.app.quantities import qlength
from metal_primitives.app.validate import require
from metal_primitives.app.shape import rounded_rectangle_wire


class RectTube(FeatureBase):
    TypeName = "MetalPrimitives::RectTube"

    def __init__(self, obj):
        super().__init__(obj)
        self._add_properties(obj)

    @staticmethod
    def _add_properties(obj):
        obj.addProperty("App::PropertyLength", "Height", "RectTube", "Extrusion length along +Z.").Height = "100 mm"
        obj.addProperty("App::PropertyLength", "Width", "RectTube", "Outer size along X.").Width = "40 mm"
        obj.addProperty("App::PropertyLength", "Depth", "RectTube", "Outer size along Y.").Depth = "20 mm"
        obj.addProperty("App::PropertyLength", "Wall", "RectTube", "Wall thickness (ignored if Solid=True).").Wall = "2 mm"

        obj.addProperty("App::PropertyLength", "OuterRadius", "RectTube", "Outer corner radius (0 for sharp).").OuterRadius = "0 mm"
        obj.addProperty("App::PropertyLength", "InnerRadius", "RectTube", "Inner corner radius (0 for sharp, ignored if Solid=True).").InnerRadius = "0 mm"

        obj.addProperty("App::PropertyBool", "Solid", "RectTube", "If True, create a solid bar (ignores Wall and InnerRadius).").Solid = False

        # Standard FreeCAD convention for stable recompute behaviour
        obj.setPropertyStatus("Placement", "-ReadOnly")  # keep movable by user

    @staticmethod
    def _validate(obj):
        H = qlength(obj.Height)
        W = qlength(obj.Width)
        D = qlength(obj.Depth)
        T = qlength(obj.Wall)
        R_out = qlength(obj.OuterRadius)
        R_in = qlength(obj.InnerRadius)
        solid = bool(obj.Solid)

        require(H > 0, "Height must be > 0")
        require(W > 0, "Width must be > 0")
        require(D > 0, "Depth must be > 0")

        require(R_out >= 0, "OuterRadius must be >= 0")
        require(R_out <= min(W, D) / 2.0, "OuterRadius must be <= min(Width, Depth)/2")

        if solid:
            require(R_in >= 0, "InnerRadius must be >= 0 (ignored when Solid=True)")
            return H, W, D, T, R_out, R_in, solid

        require(T > 0, "Wall must be > 0 when Solid=False")
        require(T < min(W, D) / 2.0, "Wall must be < min(Width, Depth)/2 when Solid=False")

        inner_w = W - 2.0 * T
        inner_d = D - 2.0 * T
        require(inner_w > 0 and inner_d > 0, "Inner dimensions must be > 0 (check Wall vs Width/Depth)")

        require(R_in >= 0, "InnerRadius must be >= 0")
        require(R_in <= min(inner_w, inner_d) / 2.0, "InnerRadius must be <= min(Width-2T, Depth-2T)/2")

        return H, W, D, T, R_out, R_in, solid

    def execute(self, obj):
        H, W, D, T, R_out, R_in, solid = self._validate(obj)

        outer = rounded_rectangle_wire(W, D, R_out)

        if solid:
            face = Part.Face(outer)
        else:
            inner_w = W - 2.0 * T
            inner_d = D - 2.0 * T
            inner = rounded_rectangle_wire(inner_w, inner_d, R_in)
            face = Part.Face([outer, inner])

        prism = face.extrude(App.Vector(0, 0, H))
        self._set_shape(obj, prism)


class RectTubeViewProvider:
    def __init__(self, vobj):
        vobj.Proxy = self

    def getIcon(self):
        # Optional: return a resource path if you want distinct icons per object type.
        return ""

    def attach(self, vobj):
        return

    def updateData(self, obj, prop):
        return

    def onChanged(self, vobj, prop):
        return

    def claimChildren(self):
        return []

    def getDisplayModes(self, vobj):
        return []

    def getDefaultDisplayMode(self):
        return "Shaded"

    def setDisplayMode(self, mode):
        return mode
