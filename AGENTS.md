# Project instructions

Before planning or modifying files, read:

`~/projects/AGENTS.md`

If the workspace policy cannot be read, stop and report that it is unavailable.

The rules below supplement or tighten the workspace policy for this repository.

## Project boundary

- This is an active-hobby FreeCAD 1.0 workbench/helper library for reusable metal primitives.
- Preserve stable documented FreeCAD APIs, expression-ready properties, single-node FeaturePython objects, and fail-fast geometric validation.
- Keep shared geometry in the existing helper structure and avoid assembly logic, undocumented FreeCAD internals, or automatic parameter clamping.
- Do not open or modify operator CAD documents as test input.

## Actual contract and done criteria

- Installation is manual copy/symlink into the user's FreeCAD modules directory; do not perform it without an explicit installation request.
- No dependency metadata, Makefile, automated tests, or CI workflow currently exists.
- Primitive changes require explicit validation cases and a report of the FreeCAD 1.0 manual verification performed or deferred.
