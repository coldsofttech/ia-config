#!/bin/bash
echo "Output files:"
for f in output/*.json; do
  echo "----- $f -----"
  cat "$f"
  echo ""
done