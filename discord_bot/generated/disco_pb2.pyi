from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_OK: _ClassVar[Result]
    RESULT_ERROR: _ClassVar[Result]
RESULT_OK: Result
RESULT_ERROR: Result

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PlayerRequest(_message.Message):
    __slots__ = ("timestamp", "name", "extra_name", "extra_message")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXTRA_NAME_FIELD_NUMBER: _ClassVar[int]
    EXTRA_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    name: str
    extra_name: str
    extra_message: str
    def __init__(self, timestamp: _Optional[int] = ..., name: _Optional[str] = ..., extra_name: _Optional[str] = ..., extra_message: _Optional[str] = ...) -> None: ...

class WithTime(_message.Message):
    __slots__ = ("timestamp",)
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    def __init__(self, timestamp: _Optional[int] = ...) -> None: ...

class ResultResponse(_message.Message):
    __slots__ = ("result", "code", "message")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    result: Result
    code: int
    message: str
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class ScheduleMessage(_message.Message):
    __slots__ = ("weekday", "start_time", "end_time")
    WEEKDAY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    weekday: int
    start_time: str
    end_time: str
    def __init__(self, weekday: _Optional[int] = ..., start_time: _Optional[str] = ..., end_time: _Optional[str] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("name", "playtime")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PLAYTIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    playtime: int
    def __init__(self, name: _Optional[str] = ..., playtime: _Optional[int] = ...) -> None: ...

class RegisterRequest(_message.Message):
    __slots__ = ("member_id", "name")
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    member_id: int
    name: str
    def __init__(self, member_id: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class ScheduleRequest(_message.Message):
    __slots__ = ("weekday",)
    WEEKDAY_FIELD_NUMBER: _ClassVar[int]
    weekday: int
    def __init__(self, weekday: _Optional[int] = ...) -> None: ...
