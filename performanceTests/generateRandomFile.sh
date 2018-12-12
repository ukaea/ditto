#!/usr/bin/env bash

dd if=/dev/urandom of="$1/1GB.bin" bs=64M count=16
