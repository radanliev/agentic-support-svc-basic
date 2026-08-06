"""
app/memory/memory_rollback.py

Rolls app/memory/store.jsonl back to a given version by dropping any
entry with version > target. Used from Week 3 (memory poisoning / agent
identity) onward. Included from Week 1 so the repository layout is
complete and stable across the whole course.

Usage:
    python -m app.memory.memory_rollback --to-version N
"""
import argparse
import json
from pathlib import Path

STORE_PATH = Path(__file__).resolve().parent / "store.jsonl"


def rollback(to_version: int) -> int:
    if not STORE_PATH.exists() or STORE_PATH.stat().st_size == 0:
        return 0
    kept = []
    with open(STORE_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("version", 0) <= to_version:
                kept.append(entry)
    with open(STORE_PATH, "w") as f:
        for entry in kept:
            f.write(json.dumps(entry) + "\n")
    return len(kept)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--to-version", type=int, required=True)
    args = parser.parse_args()
    n = rollback(args.to_version)
    print(f"memory store rolled back to version {args.to_version}: {n} entries retained")
