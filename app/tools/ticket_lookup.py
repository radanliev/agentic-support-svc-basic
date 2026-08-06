"""
app/tools/ticket_lookup.py

Looks up basic ticket metadata (status, customer) by ticket_id. Used from
Week 2 (prompt injection / tool exploitation) onward. Not exercised by the
Week 1 vulnerability demo, which targets kb_retrieve instead -- included
here so the repository layout and tool_allowlist.yaml references resolve
from the start.
"""
import json
from pathlib import Path

KB_PATH = Path(__file__).resolve().parents[2] / "fixtures" / "kb_store.json"


def ticket_lookup(ticket_id: str) -> dict:
    with open(KB_PATH) as f:
        kb = json.load(f)
    record = kb.get(ticket_id)
    if record is None:
        return {"found": False, "ticket_id": ticket_id}
    return {"found": True, "ticket_id": ticket_id, "owner": record["owner"]}
