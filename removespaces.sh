#!/bin/bash
for file in submissions/*; do mv "$file" `echo $file | tr ' ' '_'` ; done
