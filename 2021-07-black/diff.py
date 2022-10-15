#!/usr/bin/env python3

import re
import sys

pat = r"(\d+) chars:\s+(?:\d+) files changed, (\d+) insertions\(\+\), (\d+) deletions\(\-\)"

parts = {
    "core": 73308,
    "packages": 146887,
    "all": 73308 + 146887,
}
