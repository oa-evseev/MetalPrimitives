# MetalPrimitives (FreeCAD 1.0)

FeaturePython metal construction primitives with strict validation and expression-ready properties.

## Install (local, no installer)
Copy or symlink the folder `MetalPrimitives/` into one of:
- `~/.local/share/FreeCAD/Mod/`
- `~/.FreeCAD/Mod/`

Result:
- `.../Mod/MetalPrimitives/Init.py`
- `.../Mod/MetalPrimitives/InitGui.py`

Restart FreeCAD.

## Usage
1. Switch workbench to **Metal Primitives**
2. Click **RectTube** (toolbar/menu)

A single object `RectTube` is created in the document tree with editable parameters:
- Height (extrusion along +Z, base at Z=0)
- Width (X), Depth (Y)
- Wall (ignored if Solid=True)
- OuterRadius, InnerRadius (InnerRadius ignored if Solid=True)
- Solid (bool)

All length properties support expressions.

## Expressions examples
- Set `Height` to: `Spreadsheet.Length`
- Set `Wall` to: `Width * 0.05`
- Set `InnerRadius` to: `min(Width, Depth) / 10`

## Validation rules (fail-fast)
- Height > 0, Width > 0, Depth > 0
- Solid=False: 0 < Wall < min(Width, Depth)/2
- OuterRadius <= min(Width, Depth)/2
- Solid=False: InnerRadius <= min(Width-2*Wall, Depth-2*Wall)/2
Invalid parameters raise an exception on recompute.
