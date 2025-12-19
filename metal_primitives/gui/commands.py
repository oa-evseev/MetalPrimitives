import FreeCAD as App
import FreeCADGui as Gui

from metal_primitives.features.rect_tube import RectTube, RectTubeViewProvider


class CmdRectTube:
    def GetResources(self):
        return {
            "MenuText": "RectTube",
            "ToolTip": "Insert a rectangular/square hollow section (FeaturePython).",
            "Pixmap": "",  # you can put an absolute path or a Qt resource later
        }

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        doc = App.ActiveDocument
        obj = doc.addObject("Part::FeaturePython", "RectTube")
        RectTube(obj)

        if Gui.Up:
            RectTubeViewProvider(obj.ViewObject)

        doc.recompute()


def register_commands():
    Gui.addCommand("MetalPrimitives_RectTube", CmdRectTube())
