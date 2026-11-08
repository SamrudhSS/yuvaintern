# -*- coding: utf-8 -*-
"""Shared access to the measured facts produced by the reference pipeline."""

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
FACTS = json.loads((DATA / "report_facts.json").read_text(encoding="utf-8"))

SCORE = FACTS["scorecard"]
PM = SCORE["prices"]
YM = SCORE["yields"]
LOG = FACTS["log"]
PANEL = FACTS["panel"]
MANIFEST = FACTS["manifest"]
EX = FACTS["examples"]


def pct(x, dp=1):
    return f"{x * 100:.{dp}f}%"


def num(x, dp=0):
    return f"{x:,.{dp}f}"


def gate(label):
    return "pass" if SCORE["gates"].get(label) else "fail"
