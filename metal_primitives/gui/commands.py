import FreeCAD as App
import FreeCADGui as Gui

from metal_primitives.features.rect_tube import RectTube, RectTubeViewProvider
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


def register_commands():
    Gui.addCommand("MetalPrimitives_RectTube", CmdRectTube())
