from fastapi import Request

from ..container import ServiceContainer


def get_services(request: Request) -> ServiceContainer:
    return request.app.state.services


def select_api_key(body_key: str | None, header_key: str | None) -> str | None:
    return body_key or header_key
