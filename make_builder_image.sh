#!/usr/bin/env bash

BASE_SYSTEM="rocky8"

docker build --no-cache --progress plain --tag "norlook_builder:${BASE_SYSTEM}" --file "builder/${BASE_SYSTEM}.dockerfile" .
