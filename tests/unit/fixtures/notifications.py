# Copyright (c) "Neo4j"
# Neo4j Sweden AB [https://neo4j.com]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import annotations

import typing as t

import pytest


if t.TYPE_CHECKING:
    import typing_extensions as te

from neo4j import SummaryNotification


if t.TYPE_CHECKING:
    class Position(te.TypedDict):
        offset: te.NotRequired[t.Optional[int]]
        line: te.NotRequired[t.Optional[int]]
        column: te.NotRequired[t.Optional[int]]


    class TNotificationData(te.TypedDict):
        code: te.NotRequired[t.Optional[str]]
        severity: te.NotRequired[t.Optional[str]]
        title: te.NotRequired[t.Optional[str]]
        description: te.NotRequired[t.Optional[str]]
        category: te.NotRequired[t.Optional[str]]
        position: te.NotRequired[t.Optional[Position]]


    class TNotificationFactory(te.Protocol):
        def __call__(
            self,
            data: t.Optional[TNotificationData] = None,
            data_overwrite: t.Optional[TNotificationData] = None,
        ) -> SummaryNotification:
            ...


    class TRawNotificationFactory(te.Protocol):
        def __call__(
            self,
            data: t.Optional[TNotificationData] = None,
            data_overwrite: t.Optional[TNotificationData] = None,
        ) -> TNotificationData:
            ...


@pytest.fixture
def notification_factory() -> TNotificationFactory:
    def factory(
        data=None,
        data_overwrite=None,
    ) -> SummaryNotification:
        if data is None:
            data = dict(TEST_NOTIFICATION_DATA)
        if data_overwrite:
            data.update(data_overwrite)
        return SummaryNotification._from_metadata(data)

    return factory


@pytest.fixture
def raw_notification_factory() -> TRawNotificationFactory:
    def factory(
        data=None,
        data_overwrite=None,
    ) -> TNotificationData:
        if data is None:
            data = dict(TEST_NOTIFICATION_DATA)
        if data_overwrite:
            data.update(data_overwrite)
        return data

    return factory



TEST_NOTIFICATION_DATA = (
    ("title", "Some title"),
    ("code", "Neo.Made.Up.Code"),
    ("description", "Some description"),
    ("severity", "INFORMATION"),
    ("category", "HINT"),
    ("position", {"offset": 0, "line": 1, "column": 1}),
)
