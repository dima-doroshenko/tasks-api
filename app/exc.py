from typing import Literal


class HTTPExceptionModel:
    detail: str


def BadResponses(
    *statuses: int,
) -> dict[
    int,
    dict[Literal["model"], type[HTTPExceptionModel]],
]:
    return {status: {"model": HTTPExceptionModel} for status in statuses}


class NotFoundError(Exception): ...
