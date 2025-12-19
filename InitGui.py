import FreeCADGui as Gui

from metal_primitives.gui.commands import register_commands
from metal_primitives.gui.resources import WORKBENCH_NAME


class MetalPrimitivesWorkbench(Gui.Workbench):
    MenuText = WORKBENCH_NAME
    ToolTip = "Metal construction primitives (FeaturePython)."
    Icon = ""

    def Initialize(self):
        register_commands()
        self.appendToolbar(WORKBENCH_NAME, ["MetalPrimitives_RectTube"])
        self.appendMenu(WORKBENCH_NAME, ["MetalPrimitives_RectTube"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(MetalPrimitivesWorkbench())
