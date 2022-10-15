#!/bin/bash

git reset --hard HEAD
mkdir -p black/logs

cloc bin lib/spack/spack lib/spack/llnl | \
    tee black/logs/cloc.core.baseline.txt | grep Python
cloc var/spack/repos | \
    tee black/logs/cloc.packages.baseline.txt | grep Python
cloc bin lib/spack/spack lib/spack/llnl lib/spack var/spack/repos | \
    tee black/logs/cloc.all.baseline.txt | grep Python

for chars in $(seq 79 120); do
    echo -n "$chars chars:    " | tee -a black/all.txt
    echo -n "$chars chars:    " >> black/core.txt
    echo -n "$chars chars:    " >> black/packages.txt
    echo

    sed -i~ "s/line-length = .*/line-length = $chars/" pyproject.toml
    spack style --all --fix --no-isort --no-mypy --no-flake8 \
        &> "black/logs/log-${chars}.txt"

    git diff --shortstat | tee -a black/all.txt
    git diff --shortstat lib | tee -a black/core.txt
    git diff --shortstat var | tee -a black/packages.txt

    cloc bin lib/spack/spack lib/spack/llnl | \
        tee black/logs/cloc.core.$chars.txt | grep Python
    cloc var/spack/repos | \
        tee black/logs/cloc.packages.$chars.txt | grep Python
    cloc bin lib/spack/spack lib/spack/llnl lib/spack var/spack/repos | \
        tee black/logs/cloc.all.$chars.txt | grep Python
    echo

    git reset --hard HEAD
done
