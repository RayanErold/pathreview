## Week 7 — Issue selection

**Issue link:** [GitHub Issue #87](https://github.com/ascherj/pathreview/issues/87)

**Issue title:** Implement a webhook system that notifies users when their review is ready.

**Tier:** [x] Tier 3

**Problem summary:**
Long-running portfolio reviews in the assistant application currently take between 30 to 90 seconds to complete, but the system lacks any asynchronous notification mechanism. Because of this, API clients are forced to repeatedly poll the review endpoint to check if a review is completed or failed, which is highly inefficient and wastes server resources. A successful fix will introduce a database-backed webhook system affecting `api/routes` and `core/services` to allow clients to register callback URLs. When a review status changes in `review_service.py`, the system will asynchronously send a signed POST payload to the registered URL, eliminating the need for polling.

**What is lacking/affected in the codebase:**
Currently, the codebase lacks the necessary database tables, models, API endpoints, validation schemas, and service logic to support webhooks. Specifically:
- **Database & Models**: The database has no `webhooks` table, and the `User` model lacks a relationship to track registered webhooks.
- **API & Schemas**: There are no Pydantic validation schemas or REST endpoints to register, view, update, or delete webhooks.
- **Core Services**: The `review_service.py` runs processing asynchronously but has no hook to trigger external notifications, and we lack a service to securely dispatch signed HTTP payloads.

**Checklist of what we want to do:**
- [ ] Create the `Webhook` database model (`core/models/webhook.py`) and write a migration to add the `webhooks` table.
- [ ] Define the validation and response schemas (`api/schemas/webhook.py`) using Pydantic.
- [ ] Implement REST API routes (`api/routes/webhooks.py`) for webhook CRUD management with authentication.
- [ ] Build a service layer (`core/services/webhook_service.py`) for async payload dispatching and HMAC-SHA256 signature verification.
- [ ] Integrate webhook dispatching into the review lifecycle in `core/services/review_service.py` for both successful completions and processing failures.
- [ ] Implement unit tests in `tests/unit/test_webhooks.py` to verify models, services, schemas, and endpoint responses.

**Branch name:** feat/87-webhook-system-notifier

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger




## Week 8 — Reproduction & solution planning

**Reproduction commit link:** [link to commit documenting the reproduced issue]

**Reproduction summary:**
I reproduced the issue locally by running `poetry run pytest tests/unit/test_webhooks.py -v`. The test suite failed with `pydantic_core.ValidationError` due to a data type mismatch between the comma-separated string stored in the database (`events: str`) and the list expected by API schemas (`events: list[str]`), alongside `pytest` failing to execute `async def` test functions due to missing asyncio configuration in `pyproject.toml`.

**PLAN.md link:** [Plan.md](Plan.md)

**Walkthrough video (recommended):** [link to your Loom video, ≤2 min — recommended, not graded]

**Blockers or open questions:**
None.


## Week 9 — Fix implementation and validation

**Date:** 2026-08-02

**PR link:**

**Branch:**https://github.com/RayanErold/pathreview/tree/feat/87-webhook-system-notifier

**What you built:**
[1–3 sentences summarizing what your fix does and how it works]

**What I changed today:**
- Fixed webhook schema handling so `events` can be provided as either a comma-separated string or a list of strings in `api/schemas/webhook.py`.
- Added normalization logic in `core/services/webhook_service.py` to store webhook events consistently as a comma-separated string.
- Corrected `core/models/webhook.py` so a newly created `Webhook` defaults `is_active=True` and `failure_count=0` even when created directly in tests or via service constructors.
- Updated `tests/unit/test_webhooks.py` to assert `HttpUrl` fields using `str(schema.url)` and to validate webhook schema and model behavior.
- Verified the focused webhook test file passes with `py -3 -m pytest -q tests/unit/test_webhooks.py`.

**Tests added or updated:**
- `tests/unit/test_webhooks.py`

**Branch / PR notes:**
- Work is on the webhook feature branch and the focused unit tests now pass.
- [ ] Entry 1
- [ ] Entry 2

**Blockers or open questions:**
- None at this time.