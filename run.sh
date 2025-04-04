#!/bin/bash
source .venv_shoeprint/bin/activate
uvicorn backend.main:app --reload &
sleep 2
python mainv3.py
