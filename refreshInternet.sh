#!/bin/sh

while true; do
  clear
  echo refreshInternet
  dhclient -v
  sleep 1m
done