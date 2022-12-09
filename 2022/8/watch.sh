#!/bin/bash
ARGS="${@}"
clear;
while(true); do
  OUTPUT=`$ARGS`
  clear
  echo -e "${OUTPUT[@]}"
done
