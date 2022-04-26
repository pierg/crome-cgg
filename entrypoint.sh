#!/usr/bin/env bash

echo "...updating repository from server..."
git reset --hard
git config pull.rebase true
git pull


if [ $# -eq 0 ]
  then
    source run.sh
else
    source run.sh "$@"
fi