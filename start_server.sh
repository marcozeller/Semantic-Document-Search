#!/bin/bash

cd front
npm run build:watch &
cd ..
uvicorn main:app --reload