import FreeCAD as App
import Part


def rounded_rectangle_wire(wx: float, wy: float, r: float) -> Part.Wire:
    """
    Create a closed wire of a rounded rectangle in the XY plane, centered at origin.
    w: size along X, d: size along Y. r: corner radius (may be 0).
    """
    if wx <= 0 or wy <= 0:
        raise ValueError("rounded_rectangle_wire: w and d must be > 0")
    if r < 0:
        raise ValueError("rounded_rectangle_wire: r must be >= 0")

    hwx, hwy = 0.5 * wx, 0.5 * wy
    r = min(r, hwx, hwy)

    if r == 0:
        pts = [
            App.Vector(-hwx, -hwy, 0),
            App.Vector(+hwx, -hwy, 0),
            App.Vector(+hwx, +hwy, 0),
            App.Vector(-hwx, +hwy, 0),
            App.Vector(-hwx, -hwy, 0),
        ]
        return Part.makePolygon(pts)

    # Corner centers
    c1 = App.Vector(+hwx - r, +hwy - r, 0)
    c2 = App.Vector(-hwx + r, +hwy - r, 0)
    c3 = App.Vector(-hwx + r, -hwy + r, 0)
    c4 = App.Vector(+hwx - r, -hwy + r, 0)

    # Tangency points (anti-clockwise)
    p1 = App.Vector(+hwx - r, +hwy, 0)
    p2 = App.Vector(-hwx + r, +hwy, 0)
    p3 = App.Vector(-hwx, +hwy - r, 0)
    p4 = App.Vector(-hwx, -hwy + r, 0)
    p5 = App.Vector(-hwx + r, -hwy, 0)
    p6 = App.Vector(+hwx - r, -hwy, 0)
    p7 = App.Vector(+hwx, -hwy + r, 0)
    p8 = App.Vector(+hwx, +hwy - r, 0)

    # Arcs (90 deg each)
    SQRT2_OVER_2 = 0.7071067811865476
    r45 = r * SQRT2_OVER_2

    a1 = Part.Arc(p2, c2 + App.Vector(-r45,  r45, 0), p3)  # top-left
    a2 = Part.Arc(p4, c3 + App.Vector(-r45, -r45, 0), p5)  # bottom-left
    a3 = Part.Arc(p6, c4 + App.Vector( r45, -r45, 0), p7)  # bottom-right
    a4 = Part.Arc(p8, c1 + App.Vector( r45,  r45, 0), p1)  # top-right

    edges = []
    edges.append(Part.makeLine(p1, p2))   # top
    edges.append(a1.toShape())
    edges.append(Part.makeLine(p3, p4))   # left
    edges.append(a2.toShape())
    edges.append(Part.makeLine(p5, p6))   # bottom
    edges.append(a3.toShape())
    edges.append(Part.makeLine(p7, p8))   # right
    edges.append(a4.toShape())

    w = Part.Wire(edges)
    if not w.isClosed():
        raise RuntimeError("rounded_rectangle_wire: wire is not closed")
    return w
