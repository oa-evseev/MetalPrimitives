import FreeCAD as App
import Part


def rounded_rectangle_wire(w: float, d: float, r: float) -> Part.Wire:
    """
    Create a closed wire of a rounded rectangle in the XY plane, centered at origin.
    w: size along X, d: size along Y. r: corner radius (may be 0).
    """
    if w <= 0 or d <= 0:
        raise ValueError("rounded_rectangle_wire: w and d must be > 0")
    if r < 0:
        raise ValueError("rounded_rectangle_wire: r must be >= 0")

    hw, hd = 0.5 * w, 0.5 * d
    r = min(r, hw, hd)

    if r == 0:
        pts = [
            App.Vector(-hw, -hd, 0),
            App.Vector(+hw, -hd, 0),
            App.Vector(+hw, +hd, 0),
            App.Vector(-hw, +hd, 0),
            App.Vector(-hw, -hd, 0),
        ]
        return Part.makePolygon(pts)

    # Corner centers
    c1 = App.Vector(+hw - r, +hd - r, 0)
    c2 = App.Vector(-hw + r, +hd - r, 0)
    c3 = App.Vector(-hw + r, -hd + r, 0)
    c4 = App.Vector(+hw - r, -hd + r, 0)

    # Tangency points (clockwise)
    p1 = App.Vector(+hw - r, +hd, 0)
    p2 = App.Vector(-hw + r, +hd, 0)
    p3 = App.Vector(-hw, +hd - r, 0)
    p4 = App.Vector(-hw, -hd + r, 0)
    p5 = App.Vector(-hw + r, -hd, 0)
    p6 = App.Vector(+hw - r, -hd, 0)
    p7 = App.Vector(+hw, -hd + r, 0)
    p8 = App.Vector(+hw, +hd - r, 0)

    # Arcs (90 deg each)
    a1 = Part.Arc(p1, c1 + App.Vector(r, 0, 0), p8)  # top-right
    a2 = Part.Arc(p2, c2 + App.Vector(0, r, 0), p3)  # top-left
    a3 = Part.Arc(p5, c3 + App.Vector(-r, 0, 0), p4) # bottom-left
    a4 = Part.Arc(p6, c4 + App.Vector(0, -r, 0), p7) # bottom-right

    edges = []
    edges.append(Part.makeLine(p1, p2))   # top
    edges.append(a2.toShape())
    edges.append(Part.makeLine(p3, p4))   # left
    edges.append(a3.toShape())
    edges.append(Part.makeLine(p5, p6))   # bottom
    edges.append(a4.toShape())
    edges.append(Part.makeLine(p7, p8))   # right
    edges.append(a1.toShape())

    w = Part.Wire(edges)
    if not w.isClosed():
        raise RuntimeError("rounded_rectangle_wire: wire is not closed")
    return w
