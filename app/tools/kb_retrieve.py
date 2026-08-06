"""
app/tools/kb_retrieve.py

Retrieves a ticket/knowledge-base record for a given principal.

This is the file Demo 1 / Practical 1 targets. This version (v0-clean) is
the SAFE reference implementation: the ticket_id is used only as an exact
lookup key, and every result is checked against INV-1 before being
returned.

INV-1 (see ../../invariants.yaml):
    kb_retrieve must not return rows outside the requesting principal's
    ticket scope.
    Enforcement point: validate_scope() below.
    Test: tests/test_kb_retrieve.py::test_scope_containment
"""
import json
from pathlib import Path

KB_PATH = Path(__file__).resolve().parents[2] / "fixtures" / "kb_store.json"


def _load_kb() -> dict:
    with open(KB_PATH) as f:
        return json.load(f)


def validate_scope(principal: str, record: dict) -> bool:
    """INV-1 enforcement point: True only if `principal` owns `record`."""
    return record is not None and record.get("owner") == principal


def kb_retrieve(principal: str, ticket_id: str) -> dict:
    """
    Retrieve a single ticket record for `ticket_id`, scoped to `principal`.

    Returns:
        {"found": False, "ticket_id": ticket_id}
            -- no such ticket, or ticket_id is not a valid exact key
        {"found": False, "ticket_id": ticket_id, "error": "scope_violation"}
            -- ticket exists but is not owned by `principal`
        {"found": True, "ticket_id": ticket_id, "content": <str>}
            -- ticket exists and is owned by `principal`
    """
    kb = _load_kb()
    # ticket_id is used only as an exact-match dictionary key -- there is no
    # string interpolation into a query, and no pattern/operator handling.
    record = kb.get(ticket_id)

    if record is None:
        return {"found": False, "ticket_id": ticket_id}

    if not validate_scope(principal, record):
        return {"found": False, "ticket_id": ticket_id, "error": "scope_violation"}

    return {"found": True, "ticket_id": ticket_id, "content": record["content"]}
