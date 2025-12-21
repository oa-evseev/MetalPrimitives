import os
import sys

import FreeCAD as App
import FreeCADGui as Gui

class MetalPrimitivesWorkbench(Gui.Workbench):
    MenuText = "Metal Primitives"
    ToolTip = "Metal construction primitives (FeaturePython)."
    Icon = os.path.join(
        App.getUserAppDataDir(), "Mod", "MetalPrimitives", "metal_primitives", "gui", "icons", "metal_primitives_workbench.svg"
    )

    def Initialize(self):
        from metal_primitives.gui.commands import register_commands
        from metal_primitives.gui.resources import icon_path

        #self.Icon = #icon_path("metal_primitives_workbench.svg")

        register_commands()
        self.appendToolbar(self.MenuText, ["MetalPrimitives_RectTube"])
        self.appendMenu(self.MenuText, ["MetalPrimitives_RectTube"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(MetalPrimitivesWorkbench())
