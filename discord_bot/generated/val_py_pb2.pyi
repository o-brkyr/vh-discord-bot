from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class Error(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class StartedRequest(_message.Message):
    __slots__ = ("world_name", "server_name", "password", "ip_address", "port")
    WORLD_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVER_NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    world_name: str
    server_name: str
    password: str
    ip_address: str
    port: str
    def __init__(
        self,
        world_name: _Optional[str] = ...,
        server_name: _Optional[str] = ...,
        password: _Optional[str] = ...,
        ip_address: _Optional[str] = ...,
        port: _Optional[str] = ...,
    ) -> None: ...

class PlayerRequest(_message.Message):
    __slots__ = ("char_name", "member_name")
    CHAR_NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBER_NAME_FIELD_NUMBER: _ClassVar[int]
    char_name: str
    member_name: str
    def __init__(
        self, char_name: _Optional[str] = ..., member_name: _Optional[str] = ...
    ) -> None: ...
