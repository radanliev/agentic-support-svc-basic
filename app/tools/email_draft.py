"""
app/tools/email_draft.py

Drafts (and, only if approved, "sends" -- logs as sent, no real network
call) an outbound email. This is the gated, high-privilege tool used from
Week 2 (prompt injection / tool exploitation) onward to demonstrate
approval-gate enforcement. Not exercised by the Week 1 vulnerability demo.

Consults app/config/tool_allowlist.yaml. send=True is refused unless
`approved` is explicitly passed as True by the calling orchestrator.
"""
import yaml
from pathlib import Path

ALLOWLIST_PATH = Path(__file__).resolve().parents[2] / "app" / "config" / "tool_allowlist.yaml"


class ApprovalRequired(Exception):
    pass


def _policy() -> dict:
    with open(ALLOWLIST_PATH) as f:
        return yaml.safe_load(f)["email_draft"]


def email_draft(to: str, body: str, send: bool = False, attach: str = None, approved: bool = False) -> dict:
    policy = _policy()
    record = {"to": to, "body": body, "attach": attach, "send": send}

    if send and policy.get("approval_required", True) and not approved:
        record["status"] = "blocked_without_approval"
        raise ApprovalRequired(
            f"email_draft(send=True) to '{to}' requires human approval and none was given"
        )

    record["status"] = "sent" if send else "drafted"
    return record
