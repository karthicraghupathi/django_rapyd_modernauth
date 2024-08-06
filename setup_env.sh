#!/usr/bin/env bash

{
    echo 'LOG_LEVEL="INFO"'
    echo
    echo DJANGO_SECRET_KEY=\"`base64 -i /dev/urandom | head -c50`\"
    echo
} >> .env
