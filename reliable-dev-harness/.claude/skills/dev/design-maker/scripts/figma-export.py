#!/usr/bin/env python3
"""
figma-export.py - Create a Figma file from structured design YAML.
Requires FIGMA_TOKEN environment variable.
"""

import argparse
import os
import sys

import requests
import yaml

FIGMA_API = "https://api.figma.com/v1"


def create_file(token: str, name: str) -> dict:
    url = f"{FIGMA_API}/files"
    headers = {"X-Figma-Token": token, "Content-Type": "application/json"}
    payload = {"name": name}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def add_nodes(token: str, file_key: str, nodes: list) -> dict:
    # Figma REST API v1 does not support adding nodes directly.
    # This function documents the limitation and provides a plugin-based fallback.
    print("Note: Figma REST API is read-only for node manipulation.")
    print("To push nodes automatically, use the Figma MCP server or a Figma plugin.")
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Export design YAML to Figma")
    parser.add_argument("--input", required=True, help="Path to design YAML")
    parser.add_argument("--name", default="Harness Design", help="Figma file name")
    args = parser.parse_args()

    token = os.environ.get("FIGMA_TOKEN")
    if not token:
        print("Error: FIGMA_TOKEN environment variable is required.")
        print("Get your token at: https://www.figma.com/developers/api#access-tokens")
        return 1

    with open(args.input, "r", encoding="utf-8") as f:
        design = yaml.safe_load(f)

    try:
        file_info = create_file(token, args.name)
        file_key = file_info.get("key")
        print(f"Created Figma file: https://www.figma.com/file/{file_key}")
        add_nodes(token, file_key, design.get("elements", []))
        print("Done. Open the file above and use a Figma plugin or MCP server to populate nodes.")
    except requests.HTTPError as e:
        print(f"Figma API error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
