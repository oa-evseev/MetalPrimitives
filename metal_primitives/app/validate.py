from .errors import ParameterError


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise ParameterError(msg)
