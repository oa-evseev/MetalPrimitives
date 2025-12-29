import FreeCAD as App
import Part

from metal_primitives.app.feature_base import FeatureBase
from metal_primitives.app.quantities import qlength
from metal_primitives.app.validate import require


class Plate(FeatureBase):
    TypeName = "MetalPrimitives::Plate"

    def __init__(self, obj):
        super().__init__(obj)
        self._add_properties(obj)

    @staticmethod
    def _add_properties(obj):
        grp = "Plate"

        obj.addProperty("App::PropertyLength", "WidthX", grp, "Plate size along X.").WidthX = "100 mm"
        obj.addProperty("App::PropertyLength", "WidthY", grp, "Plate size along Y.").WidthY = "100 mm"
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
        wx = qlength(obj.WidthX)
        wy = qlength(obj.WidthY)
        th = qlength(obj.Thickness)

        mode = str(obj.ExtrusionMode)

        require(wx > 0, "WidthX must be > 0")
        require(wy > 0, "WidthY must be > 0")
        require(th > 0, "Thickness must be > 0")
        require(mode in ("Up", "Down", "Symmetric"), "ExtrusionMode must be one of: Up, Down, Symmetric")

        return wx, wy, th, mode

    def execute(self, obj):
        wx, wy, th, mode = self._validate(obj)

        hx = wx / 2.0
        hy = wy / 2.0

        p0 = App.Vector(-hx, -hy, 0)
        p1 = App.Vector(+hx, -hy, 0)
        p2 = App.Vector(+hx, +hy, 0)
        p3 = App.Vector(-hx, +hy, 0)

        wire = Part.makePolygon([p0, p1, p2, p3, p0])
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


class PlateViewProvider:
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
