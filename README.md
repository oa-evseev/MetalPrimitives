# MetalPrimitives (FreeCAD 1.0)

FeaturePython metal construction primitives with strict validation and expression-ready properties.

Designed for long-lived architectural and renovation models.
Focus on stable APIs, predictable behaviour, and fail-fast validation.

---

## Install (local, no installer)

Copy or symlink the folder `MetalPrimitives/` into one of:
- `~/.local/share/FreeCAD/Mod/`
- `~/.FreeCAD/Mod/`

Result:
- `.../Mod/MetalPrimitives/Init.py`
- `.../Mod/MetalPrimitives/InitGui.py`

Restart FreeCAD.

---

## Usage

1. Switch workbench to **Metal Primitives**
2. Click **RectTube** (toolbar/menu)

A single object `RectTube` is created in the document tree with editable parameters:
- Height (extrusion along +Z, base at Z=0)
- WidthX (X), WidthY (Y)
- Wall
- OuterRadius, InnerRadius

All length properties support expressions.

---

## Expressions examples

- Set `Height` to: `Spreadsheet.Length`
- Set `Wall` to: `WidthX * 0.05`
- Set `InnerRadius` to: `min(WidthX, WidthY) / 10`

---

## Validation rules (fail-fast)

- Height > 0
- WidthX > 0, WidthY > 0
- 0 < Wall < min(WidthX, WidthY) / 2
- OuterRadius ≤ min(WidthX, WidthY) / 2
- InnerRadius ≤ min(WidthX - 2*Wall, WidthY - 2*Wall) / 2

Invalid parameters raise an exception on recompute.

---

## Roadmap / TODO

### Core principles
- [x] FeaturePython objects (single tree node, no exposed internals)
- [x] Expression-ready properties (`App::PropertyLength`, etc.)
- [x] Strict parameter validation (fail-fast)
- [x] Stable, documented FreeCAD APIs only

### Hollow profiles
- [x] RectTube (RHS / SHS)
- [ ] RoundTube (CHS)
- [ ] OvalTube

### Solid profiles
- [ ] RectBar (square / rectangular)
- [ ] RoundBar
- [ ] FlatBar

### Open profiles
- [ ] Angle (L-profile, equal / unequal)
- [ ] Channel (U / C)
- [ ] I / H Beam (generic, non-standardised)
- [ ] T-profile

### Plates and sheets
- [ ] Plate (rectangular)
- [ ] Perforated plate
- [ ] Expanded metal (optional)

### UX / infrastructure
- [x] Workbench and command icons (SVG)
- [ ] Consistent property naming across all profiles
- [ ] Shared geometry utilities for profile sections
- [ ] Addon Manager metadata (`package.xml`)
- [ ] Basic documentation per primitive

---

## Non-goals (for now)

- No automatic standard tables (DIN / EN / AISC)
- No hidden auto-clamping of invalid parameters
- No multi-body or assembly logic
- No dependencies on undocumented FreeCAD internals
