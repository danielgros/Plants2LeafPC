#!/bin/bash
echo "running script"
cp ../data/images/train/* ../../3-model/dataset/train/
cp ../data/images/val/* ../../3-model/dataset/val/
python3 "2_annots_transformation.py"
