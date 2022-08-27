#!/usr/bin/env bash

{
    echo
    echo 'LOG_LEVEL="INFO"'
    echo
    echo DJANGO_SECRET_KEY=\"`base64 /dev/urandom | head -c50`\"
} >> .env
