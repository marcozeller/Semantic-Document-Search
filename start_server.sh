#!/bin/bash

source .venv/bin/activate
cd front
npm run build:watch &
cd ..
uvicorn main:app --reload