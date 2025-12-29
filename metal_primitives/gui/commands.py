import FreeCAD as App
import FreeCADGui as Gui

from metal_primitives.features.rect_tube import RectTube, RectTubeViewProvider
from metal_primitives.features.plate_triangle import PlateTriangle, PlateTriangleViewProvider
from metal_primitives.features.plate_rectangle import PlateRectangle, PlateRectangleViewProvider
from metal_primitives.gui.resources import icon_path


class CmdRectTube:
    def GetResources(self):
        return {
            "MenuText": "RectTube",
            "ToolTip": "Insert a rectangular/square hollow section (FeaturePython).",
            "Pixmap": icon_path("rect_tube.svg"),
        }

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        doc = App.ActiveDocument
        obj = doc.addObject("Part::FeaturePython", "RectTube")
        RectTube(obj)
        RectTubeViewProvider(obj.ViewObject)

        doc.recompute()

class CmdPlateTriangle:
    def GetResources(self):
        return {
            "MenuText": "PlateTriangle",
            "ToolTip": "Insert a triangular plate (gusset) defined by two sides and the included angle (FeaturePython).",
            "Pixmap": icon_path("plate_triangle.svg"),
        }

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        doc = App.ActiveDocument
        obj = doc.addObject("Part::FeaturePython", "PlateTriangle")
        PlateTriangle(obj)
        PlateTriangleViewProvider(obj.ViewObject)

        doc.recompute()

class CmdPlate:
    def GetResources(self):
        return {
            "MenuText": "PlateRectangle",
            "ToolTip": "Insert a rectangular plate (FeaturePython).",
            "Pixmap": icon_path("plate.svg"),
        }

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        doc = App.ActiveDocument
        obj = doc.addObject("Part::FeaturePython", "PlateRectangle")
        PlateRectangle(obj)
        PlateRectangleViewProvider(obj.ViewObject)

        doc.recompute()

def register_commands():
    Gui.addCommand("MetalPrimitives_RectTube", CmdRectTube())
    Gui.addCommand("MetalPrimitives_PlateTriangle", CmdPlateTriangle())
    Gui.addCommand("MetalPrimitives_PlateRectangle", CmdPlate())

