import FreeCAD as App
import Part

from metal_primitives.app.feature_base import FeatureBase
from metal_primitives.app.quantities import qlength
from metal_primitives.app.validate import require


class PlateBase(FeatureBase):
    """
    Base class for sheet-metal primitives.
    Provides Thickness + ExtrusionMode and Z-only extrusion logic.
    """

    TypeName = "MetalPrimitives::PlateBase"

    def __init__(self, obj):
        super().__init__(obj)
        self._add_plate_properties(obj)

    @staticmethod
    def _add_plate_properties(obj):
        grp = "Plate"

        obj.addProperty(
            "App::PropertyLength",
            "Thickness",
            grp,
            "Plate thickness (extrusion along Z).",
        ).Thickness = "5 mm"

        obj.addProperty(
            "App::PropertyEnumeration",
            "ExtrusionMode",
            grp,
            "Up: 0..+T, Down: -T..0, Symmetric: -T/2..+T/2.",
        )
        obj.ExtrusionMode = ["Up", "Down", "Symmetric"]
        obj.ExtrusionMode = "Up"

        obj.setPropertyStatus("Placement", "-ReadOnly")

    @staticmethod
    def _validate_plate(obj):
        th = qlength(obj.Thickness)
        mode = str(obj.ExtrusionMode)

        require(th > 0, "Thickness must be > 0")
        require(
            mode in ("Up", "Down", "Symmetric"),
            "ExtrusionMode must be one of: Up, Down, Symmetric",
        )

        return th, mode

    def _build_face(self, obj) -> Part.Face:
        """
        Must be implemented by subclasses.
        Should return a valid Part.Face in the XY plane at Z=0.
        """
        raise NotImplementedError

    def _validate(self, obj):
        """
        Subclasses may override and must call super()._validate(obj).
        """
        return self._validate_plate(obj)

    def execute(self, obj):
        th, mode = self._validate(obj)

        face = self._build_face(obj)
        if face is None or face.isNull():
            raise RuntimeError("Generated face is null")

        if mode == "Up":
            prism = face.extrude(App.Vector(0, 0, th))

        elif mode == "Down":
            prism = face.extrude(App.Vector(0, 0, -th))

        elif mode == "Symmetric":
            face0 = face.copy()
            face0.translate(App.Vector(0, 0, -th / 2.0))
            prism = face0.extrude(App.Vector(0, 0, th))

        self._set_shape(obj, prism)
