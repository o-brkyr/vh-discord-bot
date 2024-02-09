#!/bin/bash

cd discord_bot/protos

python -m grpc_tools.protoc -I. --python_out=../generated --pyi_out=../generated --grpc_python_out=../generated val_go.proto val_py.proto empty.proto