import math

import FreeCAD as App
import Part

from metal_primitives.app.feature_base import FeatureBase
from metal_primitives.app.quantities import qlength
from metal_primitives.app.validate import require


class PlateTriangle(FeatureBase):
    TypeName = "MetalPrimitives::PlateTriangle"

    def __init__(self, obj):
        super().__init__(obj)
        self._add_properties(obj)

    @staticmethod
    def _add_properties(obj):
        grp = "PlateTriangle"

        obj.addProperty("App::PropertyLength", "SideX", grp, "Side along +X from the anchor vertex.").SideX = "100 mm"
        obj.addProperty("App::PropertyLength", "SideA", grp, "Second side at Angle in the XY plane.").SideA = "100 mm"
        obj.addProperty("App::PropertyAngle", "Angle", grp, "Included angle between SideX (+X) and SideA in XY.").Angle = 90.0
        obj.addProperty("App::PropertyLength", "Thickness", grp, "Plate thickness (extrusion along Z).").Thickness = "5 mm"

        obj.addProperty(
            "App::PropertyEnumeration",
            "ExtrusionMode",
            grp,
            "Up: 0..+T, Down: -T..0, Symmetric: -T/2..+T/2.",
        )
        obj.ExtrusionMode = ["Up", "Down", "Symmetric"]
        obj.ExtrusionMode = "Up"

        obj.setPropertyStatus("Placement", "-ReadOnly")

    @staticmethod
    def _validate(obj):
        sx = qlength(obj.SideX)
        sa = qlength(obj.SideA)
        th = qlength(obj.Thickness)

        alpha_deg = float(obj.Angle.Value)
        mode = str(obj.ExtrusionMode)

        require(sx > 0, "SideX must be > 0")
        require(sa > 0, "SideA must be > 0")
        require(th > 0, "Thickness must be > 0")
        require((alpha_deg > 0.0) and (alpha_deg < 180.0), "Angle must satisfy 0 < Angle < 180 degrees")
        require(mode in ("Up", "Down", "Symmetric"), "ExtrusionMode must be one of: Up, Down, Symmetric")

        return sx, sa, th, alpha_deg, mode

    def execute(self, obj):
        sx, sa, th, alpha_deg, mode = self._validate(obj)
        alpha = math.radians(alpha_deg)

        p0 = App.Vector(0, 0, 0)
        p1 = App.Vector(sx, 0, 0)
        p2 = App.Vector(sa * math.cos(alpha), sa * math.sin(alpha), 0)

        wire = Part.makePolygon([p0, p1, p2, p0])
        face = Part.Face(wire)

        if mode == "Up":
            prism = face.extrude(App.Vector(0, 0, th))

        elif mode == "Down":
            prism = face.extrude(App.Vector(0, 0, -th))

        elif mode == "Symmetric":
            face0 = face.copy()
            face0.translate(App.Vector(0, 0, -th / 2.0))
            prism = face0.extrude(App.Vector(0, 0, th))

        self._set_shape(obj, prism)

class PlateTriangleViewProvider:
    def __init__(self, vobj):
        vobj.Proxy = self

    def getIcon(self):
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
