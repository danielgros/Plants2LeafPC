#!/bin/bash
echo "running script"
cp ../data/images/train/* ../../04-model/data/train/
cp ../data/images/val/* ../../04-model/data/val/
python3 "annots_transformation.py"
