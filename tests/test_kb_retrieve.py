"""
tests/test_kb_retrieve.py

Week 1 / Practical 1 verification suite.

Run against v0-clean: all three tests pass.
Run against v1-vulnerability (checked out later in the same session):
    test_owner_can_retrieve_own_ticket        -> still passes
    test_cannot_retrieve_other_principals_ticket -> FAILS (no scope check)
    test_scope_containment                    -> FAILS (OR-style widening)

    pytest tests/test_kb_retrieve.py -v
    pytest tests/test_kb_retrieve.py -k scope_containment -v
"""
from app.tools.kb_retrieve import kb_retrieve


def test_owner_can_retrieve_own_ticket():
    result = kb_retrieve("customer_a", "TICKET-100")
    assert result["found"] is True
    assert "Order #A1123" in result["content"]


def test_cannot_retrieve_other_principals_ticket():
    """customer_a must not be able to read customer_b's ticket (TICKET-101)."""
    result = kb_retrieve("customer_a", "TICKET-101")
    assert result["found"] is False
    assert result.get("error") == "scope_violation"


def test_scope_containment():
    """
    INV-1: kb_retrieve must not return rows outside the requesting
    principal's ticket scope, even under an attacker-controlled ticket_id.

    This is the harmless proof-of-concept from the Week 1 runbook: the
    input mimics a classic injection pattern. Against the safe
    implementation it is simply an unrecognised key (not found). Against
    the vulnerable implementation, it widens the match to every ticket in
    the store, including customer_b's -- which this test catches.
    """
    attacker_input = "TICKET-100' OR '1'='1"
    result = kb_retrieve("customer_a", attacker_input)

    if result["found"]:
        content = result["content"]
        contents = content if isinstance(content, list) else [content]
        leaked = [c for c in contents if c and "Refund #R552" in c]
        assert not leaked, (
            "scope violation: customer_a's request returned customer_b's "
            "ticket content (TICKET-101)"
        )
