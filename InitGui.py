import FreeCADGui as Gui


class MetalPrimitivesWorkbench(Gui.Workbench):
    MenuText = "Metal Primitives"
    ToolTip = "Metal construction primitives (FeaturePython)."
    Icon = ""

    def Initialize(self):
        from metal_primitives.gui.commands import register_commands

        register_commands()
        self.appendToolbar(self.MenuText, ["MetalPrimitives_RectTube"])
        self.appendMenu(self.MenuText, ["MetalPrimitives_RectTube"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(MetalPrimitivesWorkbench())
