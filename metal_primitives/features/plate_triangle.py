import math

import FreeCAD as App
import Part

from metal_primitives.app.plate_base import PlateBase
from metal_primitives.app.quantities import qlength
from metal_primitives.app.validate import require


class PlateTriangle(PlateBase):
    TypeName = "MetalPrimitives::PlateTriangle"

    def __init__(self, obj):
        super().__init__(obj)
        self._add_properties(obj)

    @staticmethod
    def _add_properties(obj):
        grp = "PlateTriangle"

        obj.addProperty(
            "App::PropertyLength",
            "SideX",
            grp,
            "Side along +X from the anchor vertex.",
        ).SideX = "100 mm"

        obj.addProperty(
            "App::PropertyLength",
            "SideA",
            grp,
            "Second side at Angle in the XY plane.",
        ).SideA = "100 mm"

        obj.addProperty(
            "App::PropertyAngle",
            "Angle",
            grp,
            "Included angle between SideX (+X) and SideA in XY.",
        ).Angle = 90.0

    def _validate(self, obj):
        th, mode = super()._validate(obj)

        sx = qlength(obj.SideX)
        sa = qlength(obj.SideA)
        alpha = float(obj.Angle.Value)

        require(sx > 0, "SideX must be > 0")
        require(sa > 0, "SideA must be > 0")
        require((alpha > 0.0) and (alpha < 180.0), "Angle must satisfy 0 < Angle < 180")

        return th, mode

    def _build_face(self, obj):
        sx = qlength(obj.SideX)
        sa = qlength(obj.SideA)
        alpha = math.radians(float(obj.Angle.Value))

        p0 = App.Vector(0, 0, 0)
        p1 = App.Vector(sx, 0, 0)
        p2 = App.Vector(sa * math.cos(alpha), sa * math.sin(alpha), 0)

        wire = Part.makePolygon([p0, p1, p2, p0])
        return Part.Face(wire)


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
