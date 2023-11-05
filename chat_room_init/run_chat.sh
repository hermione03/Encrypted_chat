#!/bin/bash

@echo off

start cmd /k "python3 server.pyy"
timeout /t 1
start cmd /k "python3 client.py"
timeout /t 1
start cmd /k "python3 client.py"
