#!/bin/bash
echo "running script"
cp ../data/images/train/* ../../03-model/data/train/
cp ../data/images/val/* ../../03-model/data/val/
python3 "2_annots_transformation.py"
