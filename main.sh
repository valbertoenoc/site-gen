#!/bin/bash

python -m src.main
cd public/ && python -m http.server 8888
