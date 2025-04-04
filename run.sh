#!/bin/bash
source .venv_shoeprint/bin/activate
uvicorn backend.main:app --reload &
sleep 2
python src/app.py
