"""Export the trained SCAN network and Streamlit feature tables for the web app."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))
from route_model import create_model  # noqa: E402


def extract_assignment(tree: ast.Module, name: str):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise KeyError(name)


def main() -> None:
    public = ROOT / "web" / "public"
    public.mkdir(parents=True, exist_ok=True)

    source = (ROOT / "app" / "web.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    catalog = {
        "salts": extract_assignment(tree, "salt_properties"),
        "solvents": extract_assignment(tree, "solvent_properties"),
    }
    (public / "features.json").write_text(
        json.dumps(catalog, separators=(",", ":")), encoding="utf-8"
    )

    model = create_model()
    model.load_state_dict(torch.load(ROOT / "app" / "1_model.pth", map_location="cpu"))
    model.eval()
    torch.onnx.export(
        model,
        (torch.zeros(1, 14), torch.zeros(1, 14), torch.zeros(1, 6)),
        public / "scan.onnx",
        input_names=["salt", "solvent", "condition"],
        output_names=["conductivity"],
        dynamic_axes={"salt": {0: "batch"}, "solvent": {0: "batch"}, "condition": {0: "batch"}},
        opset_version=17,
    )


if __name__ == "__main__":
    main()
