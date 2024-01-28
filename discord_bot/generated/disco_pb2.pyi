from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_OK: _ClassVar[Result]
    RESULT_ERROR: _ClassVar[Result]

class EventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EVENT_JOIN: _ClassVar[EventType]
    EVENT_LEAVE: _ClassVar[EventType]
    EVENT_START: _ClassVar[EventType]
    EVENT_STARTING: _ClassVar[EventType]
    EVENT_STARTED: _ClassVar[EventType]
    EVENT_STOP: _ClassVar[EventType]
    EVENT_STOPPING: _ClassVar[EventType]
    EVENT_STOPPED: _ClassVar[EventType]
    EVENT_SAVING: _ClassVar[EventType]
    EVENT_SAVED: _ClassVar[EventType]
RESULT_OK: Result
RESULT_ERROR: Result
EVENT_JOIN: EventType
EVENT_LEAVE: EventType
EVENT_START: EventType
EVENT_STARTING: EventType
EVENT_STARTED: EventType
EVENT_STOP: EventType
EVENT_STOPPING: EventType
EVENT_STOPPED: EventType
EVENT_SAVING: EventType
EVENT_SAVED: EventType

class WithUserID(_message.Message):
    __slots__ = ("userid",)
    USERID_FIELD_NUMBER: _ClassVar[int]
    userid: int
    def __init__(self, userid: _Optional[int] = ...) -> None: ...

class WithTime(_message.Message):
    __slots__ = ("timestamp",)
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    def __init__(self, timestamp: _Optional[int] = ...) -> None: ...

class WithUserIDAndTime(_message.Message):
    __slots__ = ("userid", "timestamp")
    USERID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    userid: int
    timestamp: int
    def __init__(self, userid: _Optional[int] = ..., timestamp: _Optional[int] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResultResponse(_message.Message):
    __slots__ = ("result", "code", "message")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    result: Result
    code: int
    message: str
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("event", "timestamp", "message")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    event: EventType
    timestamp: int
    message: str
    def __init__(self, event: _Optional[_Union[EventType, str]] = ..., timestamp: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class RegisterMessage(_message.Message):
    __slots__ = ("passed_name", "snowflake", "timestamp")
    PASSED_NAME_FIELD_NUMBER: _ClassVar[int]
    SNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    passed_name: str
    snowflake: int
    timestamp: int
    def __init__(self, passed_name: _Optional[str] = ..., snowflake: _Optional[int] = ..., timestamp: _Optional[int] = ...) -> None: ...
