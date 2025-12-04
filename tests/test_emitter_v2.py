# -*- coding: utf-8 -*-

import logging
from typing import Tuple
from unittest.mock import MagicMock

import pytest

from logging_loki.emitter import LokiEmitterV2

emitter_url: str = "https://example.net/loki/api/v1/push/"
headers = {"X-Scope-OrgID": "some_tenant"}
record_kwargs = {
    "name": "test",
    "level": logging.WARNING,
    "fn": "",
    "lno": "",
    "msg": "Test",
    "args": None,
    "exc_info": None,
}


@pytest.fixture()
def emitter_v2() -> Tuple[LokiEmitterV2, MagicMock]:
    """Create v2 emitter with mocked http session."""
    response = MagicMock()
    response.status_code = LokiEmitterV2.success_response_code
    session = MagicMock()
    session().post = MagicMock(return_value=response)

    instance = LokiEmitterV2(url=emitter_url, headers=headers)
    instance.session_class = session

    return instance, session


def test_init():
    LokiEmitterV2(url=emitter_url, headers=headers)
    LokiEmitterV2(url=emitter_url, headers=headers, tags={})
    LokiEmitterV2(url=emitter_url, headers=headers, tags={}, verify_ssl=True)


@pytest.fixture()
def emitter_v2_no_headers() -> Tuple[LokiEmitterV2, MagicMock]:
    """Create v2 emitter with mocked http session."""
    response = MagicMock()
    response.status_code = LokiEmitterV2.success_response_code
    session = MagicMock()
    session().post = MagicMock(return_value=response)

    instance = LokiEmitterV2(url=emitter_url)
    instance.session_class = session

    return instance, session


def create_record(**kwargs) -> logging.LogRecord:
    """Create test logging record."""
    log = logging.Logger(__name__)
    return log.makeRecord(**{**record_kwargs, **kwargs})


def get_stream(session: MagicMock) -> dict:
    """Return first stream item from json payload."""
    kwargs = session().post.call_args[1]
    streams = kwargs["json"]["streams"]
    return streams[0]


def get_request(session: MagicMock) -> dict:
    kwargs = session().post.call_args[1]
    return kwargs


def test_record_sent_to_emitter_url(emitter_v2):
    emitter, session = emitter_v2
    emitter(create_record(), "")

    got = session().post.call_args
    assert got[0][0] == emitter_url


def test_default_tags_added_to_payload(emitter_v2):
    emitter, session = emitter_v2
    emitter.tags = {"app": "emitter"}
    emitter(create_record(), "")

    stream = get_stream(session)
    level = logging.getLevelName(record_kwargs["level"]).lower()
    expected = {
        emitter.level_tag: level,
        emitter.logger_tag: record_kwargs["name"],
        "app": "emitter",
    }
    assert stream["stream"] == expected


def test_headers_added(emitter_v2):
    emitter, session = emitter_v2
    emitter.tags = {"app": "emitter"}
    emitter(create_record(), "")

    kwargs = get_request(session)
    assert kwargs["headers"]["X-Scope-OrgID"] == headers["X-Scope-OrgID"]


def test_no_headers_added(emitter_v2_no_headers):
    emitter, session = emitter_v2_no_headers
    emitter.tags = {"app": "emitter"}
    emitter(create_record(), "")

    kwargs = get_request(session)
    assert kwargs["headers"] is not None and kwargs["headers"] == {}


def test_soemthing_fun():
    import os

    a = "a"
    b = "b"
    c = "/c"
    print(os.path.join(a, b, c))
