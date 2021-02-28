import typing
import asyncio

T = typing.TypeVar('T')
def diff(past: typing.Iterable[T], pres: typing.Iterable[T]) -> typing.Union[typing.Tuple[typing.List[T], typing.List[T]], None]:
    past = set(past)
    pres = set(pres)

    growth = pres - past
    reduction = past - pres

    if len(growth) == 0 and len(reduction) == 0:
        return None
    return (list(growth), list(reduction))