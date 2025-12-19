import FreeCAD as App
import Part


class FeatureBase:
    """
    Predictable FeaturePython base:
    - strict validation in execute()
    - minimal onChanged() (optional re-validation, still fail-fast)
    """

    TypeName = "MetalPrimitives::FeatureBase"

    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, obj, prop):
        # Keep behaviour predictable: validate only on relevant props if desired.
        # Raising here is acceptable (fail-fast), but execute() remains the source of truth.
        pass

    def execute(self, obj):
        raise NotImplementedError

    @staticmethod
    def _set_shape(obj, shape: Part.Shape) -> None:
        if shape is None or shape.isNull():
            raise RuntimeError("Generated shape is null")
        obj.Shape = shape
