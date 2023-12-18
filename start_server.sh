#!/bin/bash

uvicorn main:app --reload &
cd front
npm run dev