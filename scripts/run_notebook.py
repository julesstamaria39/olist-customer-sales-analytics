"""Execute the single project notebook in place using this Python interpreter."""

from pathlib import Path
import subprocess
import sys
import time

import nbformat
from jupyter_client import KernelManager


def main():
    root = Path(__file__).resolve().parents[1]
    path = root / "notebooks" / "Final_Project.ipynb"
    ignored = {".ipynb_checkpoints", ".venv", "artifacts", ".git"}
    notebooks = [p for p in root.rglob("*.ipynb") if not ignored.intersection(p.relative_to(root).parts)]
    if notebooks != [path]:
        raise ValueError("Expected exactly one authored notebook: notebooks/Final_Project.ipynb")
    notebook = nbformat.read(path, as_version=4)
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    client = None
    started = time.monotonic()
    try:
        manager.start_kernel(cwd=str(path.parent), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        client = manager.client()
        client.start_channels()
        client.wait_for_ready(timeout=30)
        count = 0
        for cell in notebook.cells:
            if cell.cell_type != "code":
                continue
            cell.outputs = []
            cell.execution_count = None
            message_id = client.execute(cell.source)
            deadline = time.monotonic() + 180
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"Cell {cell.id} exceeded 180 seconds")
                message = client.get_iopub_msg(timeout=remaining)
                if message.get("parent_header", {}).get("msg_id") != message_id:
                    continue
                kind = message["header"]["msg_type"]
                content = message["content"]
                if kind == "execute_input":
                    cell.execution_count = content["execution_count"]
                elif kind in ("stream", "display_data", "execute_result", "error"):
                    cell.outputs.append(nbformat.v4.output_from_msg(message))
                    if kind == "error":
                        raise RuntimeError(f"Cell {cell.id}: {content['ename']}: {content['evalue']}")
                elif kind == "status" and content["execution_state"] == "idle":
                    break
            count += 1
            print(f"Executed cell {count}: {cell.id}", flush=True)
        nbformat.validate(notebook)
        nbformat.write(notebook, path)
        print(f"PASS: {count} code cells in {time.monotonic() - started:.1f}s; saved in place.")
    finally:
        if client is not None:
            client.stop_channels()
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)


if __name__ == "__main__":
    main()
