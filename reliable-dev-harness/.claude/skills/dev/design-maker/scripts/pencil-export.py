#!/usr/bin/env python3
"""
pencil-export.py - Create a minimal Pencil-compatible .epz file from design YAML.
Pencil v3 .epz is essentially a ZIP containing an XML document and metadata.
This script produces a minimal valid .epz with basic shapes mapped from YAML.
"""

import argparse
import json
import os
import sys
import zipfile
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

import yaml


def build_xml(pages: list) -> str:
    root = Element("p:Document", {
        "xmlns:p": "http://www.evolus.vn/Namespace/Pencil",
        "name": "Harness Mockup"
    })
    props = SubElement(root, "p:Properties")
    pages_el = SubElement(root, "p:Pages")

    for idx, page in enumerate(pages):
        page_el = SubElement(pages_el, "p:Page", {"id": f"page{idx}", "name": page.get("screen", f"Page {idx}")})
        content = SubElement(page_el, "p:Content")
        for el in page.get("elements", []):
            _add_shape(content, el)

    return '<?xml version="1.0"?>\n' + tostring(root, encoding="unicode")


def _add_shape(parent: Element, el: dict):
    etype = el.get("type", "box")
    x, y = el.get("position", [0, 0])
    w, h = el.get("size", [100, 40])

    if etype == "text":
        shape = SubElement(parent, "p:Shape", {"type": "Label", "x": str(x), "y": str(y)})
        text = SubElement(shape, "p:Property", {"name": "text"})
        text.text = el.get("text", "Text")
    elif etype == "button":
        shape = SubElement(parent, "p:Shape", {"type": "Rect", "x": str(x), "y": str(y), "w": str(w), "h": str(h)})
        bg = SubElement(shape, "p:Property", {"name": "fillColor"})
        bg.text = el.get("background", "#CCCCCC")
    else:
        shape = SubElement(parent, "p:Shape", {"type": "Rect", "x": str(x), "y": str(y), "w": str(w), "h": str(h)})
        border = SubElement(shape, "p:Property", {"name": "strokeColor"})
        border.text = el.get("border_color", "#000000")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export design YAML to Pencil .epz")
    parser.add_argument("--input", required=True, help="Path to design YAML")
    parser.add_argument("--output", default="mockup.epz", help="Output .epz path")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        design = yaml.safe_load(f)

    pages = design if isinstance(design, list) else [design]
    xml_content = build_xml(pages)

    out_path = Path(args.output)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.xml", xml_content)
        zf.writestr("meta.json", json.dumps({"version": "3.1.1", "app": "Pencil"}))

    print(f"Created Pencil mockup: {out_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
