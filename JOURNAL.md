## Week 7 — Issue selection

**Issue link:** [GitHub Issue #87](https://github.com/ascherj/pathreview/issues/87)

**Issue title:** Implement a webhook system that notifies users when their review is ready

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

**Branch name:** feature/87-webhook-system-notifier

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger