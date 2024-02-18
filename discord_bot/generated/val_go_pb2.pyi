from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleMessage(_message.Message):
    __slots__ = ("weekday", "sessions")
    WEEKDAY_FIELD_NUMBER: _ClassVar[int]
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    weekday: int
    sessions: _containers.RepeatedCompositeFieldContainer[Session]
    def __init__(
        self,
        weekday: _Optional[int] = ...,
        sessions: _Optional[_Iterable[_Union[Session, _Mapping]]] = ...,
    ) -> None: ...

class Session(_message.Message):
    __slots__ = ("start_time", "end_time", "player_count")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    PLAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    start_time: str
    end_time: str
    player_count: int
    def __init__(
        self,
        start_time: _Optional[str] = ...,
        end_time: _Optional[str] = ...,
        player_count: _Optional[int] = ...,
    ) -> None: ...

class ScheduleRequest(_message.Message):
    __slots__ = ("weekday", "session")
    WEEKDAY_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    weekday: int
    session: Session
    def __init__(
        self,
        weekday: _Optional[int] = ...,
        session: _Optional[_Union[Session, _Mapping]] = ...,
    ) -> None: ...

class QueryPlayersResponse(_message.Message):
    __slots__ = ("online", "player_list")
    ONLINE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_LIST_FIELD_NUMBER: _ClassVar[int]
    online: bool
    player_list: _containers.RepeatedCompositeFieldContainer[PlayerData]
    def __init__(
        self,
        online: bool = ...,
        player_list: _Optional[_Iterable[_Union[PlayerData, _Mapping]]] = ...,
    ) -> None: ...

class PlayerData(_message.Message):
    __slots__ = ("char_name", "member_name", "playtime_s")
    CHAR_NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBER_NAME_FIELD_NUMBER: _ClassVar[int]
    PLAYTIME_S_FIELD_NUMBER: _ClassVar[int]
    char_name: str
    member_name: str
    playtime_s: int
    def __init__(
        self,
        char_name: _Optional[str] = ...,
        member_name: _Optional[str] = ...,
        playtime_s: _Optional[int] = ...,
    ) -> None: ...

class QueryStatusResponse(_message.Message):
    __slots__ = ("status",)
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RESULT_STARTING: _ClassVar[QueryStatusResponse.Status]
        RESULT_STARTED: _ClassVar[QueryStatusResponse.Status]
        RESULT_STOPPING: _ClassVar[QueryStatusResponse.Status]
        RESULT_STOPPED: _ClassVar[QueryStatusResponse.Status]
        RESULT_ERROR: _ClassVar[QueryStatusResponse.Status]
    RESULT_STARTING: QueryStatusResponse.Status
    RESULT_STARTED: QueryStatusResponse.Status
    RESULT_STOPPING: QueryStatusResponse.Status
    RESULT_STOPPED: QueryStatusResponse.Status
    RESULT_ERROR: QueryStatusResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: QueryStatusResponse.Status
    def __init__(
        self, status: _Optional[_Union[QueryStatusResponse.Status, str]] = ...
    ) -> None: ...

class RegisterRequest(_message.Message):
    __slots__ = ("snowflake", "char_name")
    SNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    CHAR_NAME_FIELD_NUMBER: _ClassVar[int]
    snowflake: int
    char_name: str
    def __init__(
        self, snowflake: _Optional[int] = ..., char_name: _Optional[str] = ...
    ) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ("characters",)
    CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    characters: _containers.RepeatedCompositeFieldContainer[PlayerData]
    def __init__(
        self, characters: _Optional[_Iterable[_Union[PlayerData, _Mapping]]] = ...
    ) -> None: ...
