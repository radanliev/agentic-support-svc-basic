"""
app/agent.py

Minimal orchestrator used across the demo series: given a principal and a
ticket_id, it calls the kb_retrieve tool and returns the result. The demos
are about the security boundary around each tool call, not about agent
planning sophistication, so this stays deliberately small.

Week 1 usage (from the repository root, with the venv active):

    python -m app.agent customer_a TICKET-100
    python -m app.agent customer_a "TICKET-100' OR '1'='1"
"""
import sys

from app.tools.kb_retrieve import kb_retrieve


def handle_ticket_request(principal: str, ticket_id: str) -> dict:
    return kb_retrieve(principal, ticket_id)


if __name__ == "__main__":
    principal = sys.argv[1] if len(sys.argv) > 1 else "customer_a"
    ticket_id = sys.argv[2] if len(sys.argv) > 2 else "TICKET-100"
    result = handle_ticket_request(principal, ticket_id)
    print(result)
