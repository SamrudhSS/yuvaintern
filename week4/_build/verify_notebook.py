# -*- coding: utf-8 -*-
"""Post-execution checks for the executed notebook."""

import sys
from pathlib import Path

import nbformat

HERE = Path(__file__).resolve().parent
NOTEBOOK = HERE.parent / "notebooks" / "Agribusiness_Predictive_Modelling_Pipeline.ipynb"

nb = nbformat.read(NOTEBOOK, as_version=4)
nbformat.validate(nb)

code_cells = [c for c in nb.cells if c.cell_type == "code"]
executed = [c for c in code_cells if c.get("execution_count")]
errors = []
images = 0
streams = []
for i, cell in enumerate(nb.cells):
    for output in cell.get("outputs", []):
        if output.output_type == "error":
            errors.append((i, output.ename, output.evalue))
        if output.output_type == "display_data" and "image/png" in output.get("data", {}):
            images += 1
        if output.output_type == "stream":
            streams.append(output.text)

text = "".join(streams)
print(f"cells={len(nb.cells)} code={len(code_cells)} executed={len(executed)} images={images} errors={len(errors)}")
for err in errors:
    print("ERROR", err)
print(f"stream ConvergenceWarning={text.count('ConvergenceWarning')} Traceback={text.count('Traceback')}")

required = [
    HERE.parent / "data" / "notebook_model_scorecard.csv",
    HERE.parent / "data" / "notebook_cross_commodity.csv",
    HERE.parent / "data" / "notebook_latest_forecast.csv",
]
for path in required:
    print(f"{'OK ' if path.exists() else 'MISSING'} {path.name} {path.stat().st_size if path.exists() else 0} bytes")

if errors or len(executed) != len(code_cells):
    sys.exit(1)
print("PASS: executed notebook is valid, complete, and error-free")
