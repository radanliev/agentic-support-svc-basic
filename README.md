# agentic-support-svc

Shared synthetic repository for the bootcamp. All data, credentials, and
endpoints are fake and local. Nothing in this repository talks to a real
service.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.lock
pytest tests/ -v                  # should be 3 passed, on v0-clean
```

## Tag convention

| Tag | Used in | Expected condition |
|---|---|---|
| `v0-clean` | Baseline | Benign functionality, documented permissions, no planted defects. |
| `v1-vulnerability` | Week 1 | Unsanitised `ticket_id` handling and a widened service-account role. |
| `v2-supply-chain-drift` | Week 4 | Dependency, workflow, AIBOM, and role-binding drift. |
| `v3-poisoned-memory` | Week 3 | Unsigned memory entry; malicious ticket fixture available alongside it. |
| `v4-controls-applied` | Week 4 | Full evidence bundle, used as the passing baseline before defect injection. |

Only `v0-clean` and `v1-vulnerability` exist yet — this is the Week 1 build.
Later tags are scaffolded but not yet populated; do not check them out
until the corresponding week's repository update lands.

---

## Week 1 — Software Vulnerabilities & Executable Security Properties

**Outcome:** a vulnerability claim is only as strong as the source-linked
model and test that back it.

### Live runbook

**1. [Claude Code]** On `v0-clean`, open the repository and derive
`threat_model.yaml` blind: list every principal, trust boundary, and
asset, tag each with a STRIDE-for-agents category, and cite `file:line`
for every edge. This is a prediction — the vulnerable tag has not been
checked out yet.

```bash
git checkout v0-clean
# work with Claude Code against this checkout; save its output over
# threat_model.yaml (currently an empty stub with the schema in comments)
```

**2. [GitHub Copilot]** Working from `threat_model.yaml` alone, draft a
defensive patch for the boundary Claude Code flagged as weakest — before
the real defect is shown. Save the diff; do not apply it yet.

**3. Reveal the defect**

```bash
git checkout v1-vulnerability
git diff v0-clean v1-vulnerability -- app/tools/kb_retrieve.py deploy/service-account.yaml
```

This reveals: `app/tools/kb_retrieve.py` no longer checks ticket
ownership and treats `ticket_id` as a pattern rather than an exact key,
and `deploy/service-account.yaml` has been widened from `read-only` to
`read-write`.

**4. [Cursor]** Independently trace the vulnerable path from this
checkout — without reading Claude Code's model or Copilot's draft patch —
and confirm `tests/test_kb_retrieve.py` already encodes the check
(`test_scope_containment`, `test_cannot_retrieve_other_principals_ticket`).

```bash
pytest tests/test_kb_retrieve.py -v
```

Expected on `v1-vulnerability`: **2 failed, 1 passed.**

**5. Compare.** Line up Claude Code's blind prediction, Cursor's
independent trace, and Copilot's draft patch. Do all three converge on
`app/tools/kb_retrieve.py`?

**6. [GitHub Copilot]** Revise the patch using the confirmed defect. The
fix is to restore ownership validation and treat `ticket_id` as an exact
key only (see `v0-clean`'s version of the file for the reference
implementation), and revert the service-account role to `read-only`.

**7. Verify.**

```bash
pytest tests/test_kb_retrieve.py -v
```

Expected after the patch: **3 passed.**

### Harmless proof-of-concept used in step 4/7

```bash
source venv/bin/activate
python -m app.agent customer_a "TICKET-100' OR '1'='1"
```

On `v1-vulnerability` this returns every ticket in the local mock store,
including `customer_b`'s (`TICKET-101`) — a scope-widening bug in a
synthetic, offline JSON file, not a real data exposure. On `v0-clean` or
the patched version it returns `{"found": False, ...}` because the string
is not a valid ticket key.

### Evidence to capture

- `threat_model.yaml` (Claude Code's blind prediction)
- `git diff v0-clean v1-vulnerability`
- Cursor's independent trace notes
- Copilot's before/after patch diff
- `pytest` output before and after the patch (paste both into
  `evidence/week1.md`)

### Proof frame

- **Conceptual leap:** a structured model can locate a real defect before
  it is revealed, not just explain one after the fact.
- **Physical proof-of-concept:** the `OR`-pattern PoC above, run against a
  local mock store, with a parameterised/scope-checked fix that removes
  it.
- **Reproducibility:** fixed tag pair, fixed prompt template, fixed test
  names — anyone can rerun this and get the same red-then-green result.
- **Novel physical testing:** the blind-prediction-then-reveal protocol —
  Copilot patches before the defect is shown, Cursor traces
  independently, and the three outputs are scored for convergence.
- **Live verification:** `pytest` is run in front of the room: red on
  `v1-vulnerability`, green once the patch lands.

---

## Repository layout

```
agentic-support-svc/
├── app/
│   ├── agent.py                # orchestrator
│   ├── tools/{kb_retrieve.py, ticket_lookup.py, email_draft.py}
│   ├── memory/{store.jsonl, memory_rollback.py}
│   └── config/{identity.yaml, permissions.yaml, tool_allowlist.yaml}
├── deploy/{Dockerfile, manifest.yaml, service-account.yaml}
├── fixtures/{kb_store.json, tickets/}
├── tests/
├── requirements.lock
├── aibom.json
├── threat_model.yaml            # empty stub, filled live in Week 1 / Week 3
├── invariants.yaml              # INV-1 pre-populated (matches tests/)
├── model_config.yaml
└── pyproject.toml
```

`app/tools/ticket_lookup.py`, `app/tools/email_draft.py`,
`app/memory/`, and `app/config/identity.yaml` are not exercised by Week 1
— they're included now so the layout is stable and later weeks don't
require restructuring.

## Safety rules

- Synthetic data, fake credentials, local-only services. Nothing here
  reaches a real system.
- Treat any AI-generated patch as untrusted until the test suite confirms
  it.
- Reset to `v0-clean` between sessions: `git checkout v0-clean`.
