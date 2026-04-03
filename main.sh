#!/bin/bash

python -m src.main
cd docs/ && python -m http.server 8888
