import FreeCAD as App
import Part

from metal_primitives.app.plate_base import PlateBase
from metal_primitives.app.quantities import qlength
from metal_primitives.app.validate import require


class PlateRectangle(PlateBase):
    TypeName = "MetalPrimitives::PlateRectangle"

    def __init__(self, obj):
        super().__init__(obj)
        self._add_properties(obj)

    @staticmethod
    def _add_properties(obj):
        grp = "PlateRectangle"

        obj.addProperty("App::PropertyLength", "WidthX", grp, "Plate size along X.").WidthX = "100 mm"
        obj.addProperty("App::PropertyLength", "WidthY", grp, "Plate size along Y.").WidthY = "100 mm"

    def _validate(self, obj):
        th, mode = super()._validate(obj)

        wx = qlength(obj.WidthX)
        wy = qlength(obj.WidthY)

        require(wx > 0, "WidthX must be > 0")
        require(wy > 0, "WidthY must be > 0")

        return th, mode

    def _build_face(self, obj):
        wx = qlength(obj.WidthX)
        wy = qlength(obj.WidthY)

        hx = wx / 2.0
        hy = wy / 2.0

        p0 = App.Vector(-hx, -hy, 0)
        p1 = App.Vector(+hx, -hy, 0)
        p2 = App.Vector(+hx, +hy, 0)
        p3 = App.Vector(-hx, +hy, 0)

        wire = Part.makePolygon([p0, p1, p2, p3, p0])
        return Part.Face(wire)


class PlateRectangleViewProvider:
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
