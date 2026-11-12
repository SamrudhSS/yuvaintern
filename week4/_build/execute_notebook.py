# -*- coding: utf-8 -*-
"""Execute the generated notebook and persist the real outputs."""

from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
NOTEBOOK = HERE.parent / "notebooks" / "Agribusiness_Predictive_Modelling_Pipeline.ipynb"

nb = nbformat.read(NOTEBOOK, as_version=4)
nbformat.validate(nb)

client = NotebookClient(
    nb,
    timeout=2400,
    kernel_name="python3",
    resources={"metadata": {"path": str(NOTEBOOK.parent)}},
    allow_errors=False,
)
client.execute()

nbformat.write(nb, NOTEBOOK)
print(f"Executed and saved {NOTEBOOK}")
print(f"Cells: {len(nb.cells)} | code cells: {sum(c.cell_type == 'code' for c in nb.cells)}")
