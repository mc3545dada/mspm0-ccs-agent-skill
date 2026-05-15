#!/usr/bin/env python3
"""Index MSPM0 SDK SysConfig examples and module metadata."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ADD_MODULE_RE = re.compile(r"scripting\.addModule\(\s*[\"']/ti/driverlib/([^\"']+)[\"']")
BOARD_PREFIXES = ("LP_", "MSPM0")
SKIP_DIRS = {".git", ".svn", ".hg", "__pycache__"}


@dataclass
class SyscfgExample:
    path: str
    board: str | None
    modules: list[str]


@dataclass
class ModuleMetadata:
    module: str
    path: str


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def iter_files(root: Path, suffix: str) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(suffix):
                yield Path(dirpath) / filename


def infer_board(path: Path, sdk_root: Path) -> str | None:
    parts = path.relative_to(sdk_root).parts
    for part in parts:
        if part.startswith(BOARD_PREFIXES):
            return part
    return None


def modules_from_syscfg(path: Path) -> list[str]:
    text = read_text(path)
    modules = {match.group(1).split("/")[-1].upper() for match in ADD_MODULE_RE.finditer(text)}
    return sorted(modules)


def find_examples(sdk_root: Path) -> list[SyscfgExample]:
    examples_root = sdk_root / "examples"
    if not examples_root.exists():
        return []

    examples: list[SyscfgExample] = []
    for path in sorted(iter_files(examples_root, ".syscfg")):
        examples.append(
            SyscfgExample(
                path=rel(path, sdk_root),
                board=infer_board(path, sdk_root),
                modules=modules_from_syscfg(path),
            )
        )
    return examples


def find_metadata(sdk_root: Path) -> list[ModuleMetadata]:
    meta_root = sdk_root / "source" / "ti" / "driverlib" / ".meta"
    if not meta_root.exists():
        return []

    metadata: list[ModuleMetadata] = []
    for path in sorted(iter_files(meta_root, ".syscfg.js")):
        name = path.name.removesuffix(".syscfg.js").upper()
        metadata.append(ModuleMetadata(module=name, path=rel(path, sdk_root)))
    return metadata


def split_filters(values: list[str] | None) -> set[str]:
    if not values:
        return set()
    filters: set[str] = set()
    for value in values:
        for part in value.split(","):
            part = part.strip().upper()
            if part:
                filters.add(part)
    return filters


def matches_module(example: SyscfgExample, modules: set[str]) -> bool:
    if not modules:
        return True
    path_upper = example.path.upper()
    return bool(set(example.modules) & modules) or any(module in path_upper for module in modules)


def matches_board(example: SyscfgExample, board: str | None) -> bool:
    if not board:
        return True
    board_upper = board.upper()
    return board_upper in example.path.upper() or bool(example.board and board_upper in example.board.upper())


def filter_examples(
    examples: list[SyscfgExample],
    modules: set[str],
    board: str | None,
) -> list[SyscfgExample]:
    return [example for example in examples if matches_module(example, modules) and matches_board(example, board)]


def group_examples_by_module(
    examples: list[SyscfgExample],
    module_filters: set[str] | None = None,
) -> dict[str, list[SyscfgExample]]:
    grouped: dict[str, list[SyscfgExample]] = {}
    for example in examples:
        if module_filters:
            modules = sorted(module for module in module_filters if module in example.modules or module in example.path.upper())
        else:
            modules = example.modules or ["UNKNOWN"]
        for module in modules:
            grouped.setdefault(module, []).append(example)
    return dict(sorted(grouped.items()))


def print_report(
    sdk_root: Path,
    examples: list[SyscfgExample],
    metadata: list[ModuleMetadata],
    limit: int,
    module_filters: set[str],
) -> None:
    print(f"SDK root: {sdk_root}")
    print(f"SysConfig examples: {len(examples)}")
    print(f"Module metadata files: {len(metadata)}")
    print()

    if metadata:
        print("Available module metadata:")
        for item in metadata:
            print(f"  - {item.module}: {item.path}")
        print()
    else:
        print("WARNING: No module metadata found under source/ti/driverlib/.meta")
        print()

    if not examples:
        print("WARNING: No .syscfg examples found under examples/")
        return

    print("Examples by module:")
    grouped = group_examples_by_module(examples, module_filters)
    for module, items in grouped.items():
        print(f"[{module}] {len(items)} example(s)")
        for example in items[:limit]:
            board = f" ({example.board})" if example.board else ""
            modules = ",".join(example.modules) if example.modules else "no addModule calls detected"
            print(f"  - {example.path}{board} [{modules}]")
        if len(items) > limit:
            print(f"  ... {len(items) - limit} more")
        print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Index MSPM0 SDK .syscfg examples and SysConfig module metadata.",
    )
    parser.add_argument("sdk_root", help="Path to the MSPM0 SDK root, such as C:\\ti\\mspm0_sdk_2_10_00_04")
    parser.add_argument("--module", "-m", action="append", help="Filter by module name, e.g. UART,GPIO,DMA")
    parser.add_argument("--board", "-b", help="Filter by board/path substring, e.g. LP_MSPM0G3507")
    parser.add_argument("--limit", type=int, default=20, help="Maximum examples printed per module group")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sdk_root = Path(args.sdk_root).expanduser().resolve()
    if not sdk_root.exists():
        print(f"ERROR: SDK root does not exist: {sdk_root}", file=sys.stderr)
        return 2
    if not sdk_root.is_dir():
        print(f"ERROR: SDK root is not a directory: {sdk_root}", file=sys.stderr)
        return 2

    module_filters = split_filters(args.module)
    examples = filter_examples(find_examples(sdk_root), module_filters, args.board)
    metadata = find_metadata(sdk_root)
    if module_filters:
        metadata = [item for item in metadata if item.module in module_filters]

    if args.json:
        payload = {
            "sdk_root": str(sdk_root),
            "examples": [asdict(example) for example in examples],
            "metadata": [asdict(item) for item in metadata],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_report(sdk_root, examples, metadata, max(args.limit, 1), module_filters)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
