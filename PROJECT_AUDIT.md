# TRACE × X — Master Project Audit
**Authoritative Architectural Inspection & Vulnerability Assessment**
*Department of Computer Science & Engineering | T.J.S. Engineering College*

---

## 1. Existing Architecture & System Overview

The TRACE × X application is a hybrid Single-Page Application (SPA) and multi-page web platform designed for technical cybersecurity competition hosting, active proctoring, live incident response triage, and administrative event lifecycle management.

* **Backend Framework**: Python 3 standard library `HTTPServer` with a custom `TraceXRequestHandler` ([server.py](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/server.py)).
* **Database Engine**: SQLite 3 ([tracex.db](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/tracex.db)) with 15 tables, foreign keys, row factory mapping, and atomic SQLite backup API integration.
* **Frontend Structure**:
  - `index.html`: Unified SPA container featuring view switching between `#view-homepage`, `#view-case-selection`, and `#view-investigation`.
  - Secondary Multi-page entry points: `login.html`, `register.html`, `cases.html`, `investigation.html`, `evaluation.html`, `results.html`, `rules.html`, `admin-login.html`, and `admin.html`.
  - Styling: Pure Vanilla CSS ([assets/css/style.css](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/css/style.css) and [rules.css](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/rules.css)).
  - Scripting: Vanilla ES6 modules ([assets/js/app.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/app.js), [assets/js/admin.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/admin.js), and [assets/js/investigation-data.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/investigation-data.js)).

---

## 2. Existing Routes & Pages

### Frontend Pages
* `/` or `/index.html`: Main mission hub, Option 1 dual-slash cinematic intro sequence, fingerprint HUD graphic, and view container.
* `/login.html`: Participant login portal with Team ID and PIN inputs.
* `/register.html`: Team registration portal supporting 1–4 member rosters.
* `/cases.html`: Redirect router wrapper forwarding to `index.html#cases`.
* `/investigation.html`: Redirect router wrapper forwarding to `index.html#investigation`.
* `/evaluation.html`: 5-Minute automated evaluation screen.
* `/results.html`: Final participant results and standing screen.
* `/rules.html`: Official rules and regulations handbook.
* `/admin-login.html`: Administrator authentication portal.
* `/admin.html`: Administrator control console with 10 management protocols.

### Active Backend API Routes
* **Public / Participant Endpoints**:
  - `GET /api/health`
  - `GET /api/event/status`
  - `GET /api/cases`
  - `GET /api/cases/questions`
  - `GET /api/round/timer`
  - `POST /api/teams/register`
  - `POST /api/round/submit-early`
  - `POST /api/round/auto-submit`
* **Protected Administrator Endpoints**:
  - `POST /api/admin/login`
  - `POST /api/admin/logout`
  - `GET /api/admin/overview`
  - `GET /api/admin/teams`
  - `GET /api/admin/sessions`
  - `GET /api/admin/round-control`
  - `POST /api/admin/event-control`
  - `POST /api/admin/round-control`
  - `GET /api/admin/violations`
  - `GET /api/admin/evaluations`
  - `POST /api/admin/results-action`
  - `POST /api/admin/override-result`
  - `GET /api/admin/settings`
  - `POST /api/admin/settings`
  - `GET /api/admin/report`
  - `POST /api/admin/report/create`
  - `POST /api/admin/report/save`
  - `POST /api/admin/report/status`
  - `POST /api/admin/report/restore`
  - `POST /api/admin/report/new-revision`
  - `GET /api/admin/cases`
  - `GET /api/admin/cases/detail`
  - `GET /api/admin/cases/validation`
  - `POST /api/admin/cases/save`
  - `POST /api/admin/cases/delete`
  - `POST /api/admin/questions/save`
  - `POST /api/admin/questions/delete`
  - `POST /api/admin/questions/reorder`
  - `GET /api/admin/audit-logs`
  - `GET /api/admin/export/teams`
  - `GET /api/admin/export/results`
  - `GET /api/admin/export/violations`
  - `GET /api/admin/export/report`
  - `GET /api/admin/export/history`
  - `GET /api/admin/backups`
  - `POST /api/admin/backups/create`
  - `GET /api/admin/backups/download`
  - `POST /api/admin/backups/delete`

---

## 3. Current Data Models (SQLite 3 Schema)

1. `admins`: Admin ID, PBKDF2 hash, salt, name, role, created_at.
2. `admin_sessions`: Bearer token, admin ID, created_at, expires_at.
3. `teams`: Team ID, team name, college, department, team size, members JSON, masked PIN, hashed PIN, salt, registered_at, status.
4. `sessions`: Team ID, case ID, case name, current round, current question, time remaining, connection status, session status, updated_at.
5. `violations`: ID, team ID, violation type, timestamp, violation count, action taken.
6. `submissions`: Team ID, case ID, round1_answers_json, round2_answers_json, score_r1, score_r2, total_score, accuracy_rate, violations_count, evaluation_status, qualification_status, submitted_at.
7. `event_state`: Key/value store for event state, round, settings JSON, timestamps.
8. `audit_logs`: ID, admin ID, action, details, prev value, new value, timestamp.
9. `event_reports`: Official report metadata, overview JSON, participation JSON, structure JSON, results JSON, summary JSON, organizers JSON.
10. `event_report_versions`: Snapshots of event reports for revision tracking and rollbacks.
11. `cases`: Case ID, name, summary, evidence JSON, round 2 evidence JSON, status, order_idx.
12. `questions`: ID, case ID, round, order num, question text, options A-D, correct answer, marks, evidence ref.
13. `backups`: ID, backup ID, filename, file path, size, created by, timestamp, status.
14. `export_logs`: ID, export type, format, admin ID, timestamp, status, record count.
15. `round_timers`: ID, team ID, case ID, round, start time ms, end time ms, duration sec, is submitted early, submitted at ms.

---

## 4. Confirmed Logic Bugs & Deficiencies

### Bug 1: Participant Login Uses Client SessionStorage Instead of Backend Verification
* **Location**: [assets/js/app.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/app.js#L547-L572) & [server.py](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/server.py)
* **Finding**: `initLogin()` in `app.js` checks `sessionStorage.getItem('traceX_registeredTeams')` for plaintext PIN matching instead of authenticating against the backend SQLite database. `server.py` does NOT possess a `/api/teams/login` endpoint. Consequently, a team registered on one computer/tab cannot log in from another browser or after clearing session storage.

### Bug 2: Answers Are Stored in Submissions but Never Evaluated on the Backend
* **Location**: [server.py](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/server.py#L1541-L1623)
* **Finding**: Endpoints `/api/round/submit-early` and `/api/round/auto-submit` update `round1_answers_json` and `round2_answers_json` in the `submissions` table, but no backend logic ever scores those answers against the authoritative `questions` table. `score_r1`, `score_r2`, `total_score`, and `accuracy_rate` remain `0` (or the initial seed placeholder) and `evaluation_status` remains `PENDING`.

### Bug 3: Participant Question Answer Keys Leaked in Client-Side Dataset
* **Location**: [assets/js/investigation-data.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/investigation-data.js)
* **Finding**: The client script `investigation-data.js` includes the `"answer": <index>` property directly on every question object. Anyone opening DevTools can inspect `TRACE_INVESTIGATION_CASES` to view all correct answers.

### Bug 4: Participant Fullscreen Exits on Cross-Page Navigation
* **Location**: [login.html](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/login.html#L217-L220) & [assets/js/app.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/app.js#L618-L635)
* **Finding**: When a participant clicks "[ ENTER FULLSCREEN & CONTINUE ]" on `login.html`, `requestFullscreen()` activates, but the script then calls `window.location.href = 'index.html'`. Standard browser security models drop HTML5 Fullscreen on cross-document navigation, breaking the required persistent fullscreen requirement.

### Bug 5: Missing Participant Violation Logging Endpoint
* **Location**: [assets/js/app.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/app.js#L1714-L1755) & [server.py](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/server.py)
* **Finding**: Client-side proctoring increments `violationCount` in `sessionStorage`, but does not transmit violation incidents to the backend SQLite `violations` table. Administrators cannot see real live violations triggered by candidates.

### Bug 6: Admin Event Start Does Not Initialize Official Round Timestamps
* **Location**: [server.py](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/server.py#L1641-L1674)
* **Finding**: In `/api/admin/event-control` (`action == 'start'`), `server.py` updates `status = 'EVENT ACTIVE'`, but fails to create `round1_start_time` and `round1_end_time` in `event_state`. Furthermore, `/api/round/timer` creates private per-team timers when no event-wide timestamp is present, instead of holding all teams in a synchronized STANDBY state before event commencement.

### Bug 7: Participant Results Route Calls Protected Admin Endpoint
* **Location**: [assets/js/app.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/app.js#L2400-L2405)
* **Finding**: `initResults()` calls `/api/admin/settings` to determine `resultsPublished`. However, `/api/admin/settings` requires administrator Bearer token authentication (returns 401 for participants). A dedicated, unauthenticated public participant result endpoint is missing.

---

## 5. Security Concerns

1. **Exposed Answer Keys**: Client-side `investigation-data.js` holds answer indexes for all 450 questions.
2. **Plaintext Session Verification**: Client-side login checks `t.pinRaw === pinVal` from `sessionStorage`.
3. **Unprotected Participant URLs**: Anyone manipulating URL query parameters can query other team IDs if not scoped to active session tokens or authenticated cookies.
4. **Missing Rate Limiting**: Registration and login endpoints have no brute-force rate-limiting wrappers.

---

## 6. Required Database & Backend Changes

1. **Add `/api/teams/login`**:
   - Accepts `teamId` and `pin`.
   - Looks up `teams` where `team_id = ?`.
   - Validates PIN using `verify_password(pin, row['pin_hash'], row['pin_salt'])`.
   - Returns official team dossier and sets session cookies/tokens.
2. **Add `/api/violations/log`**:
   - Accepts `teamId`, `violationType`, `violationCount`, and `actionTaken`.
   - Inserts into `violations` table and increments `violations_count` in `submissions`.
   - If count >= 3, automatically sets qualification status to `DISQUALIFIED` and marks session as terminated.
3. **Add `/api/participant/result`**:
   - Accepts `team_id`.
   - Checks `event_state.settings.resultsPublished`.
   - If `false`, returns `{ status: "RESULTS UNDER REVIEW", isPublished: false }`.
   - If `true`, returns ONLY the calling team's qualification status (`QUALIFIED`, `NOT QUALIFIED`, `DISQUALIFIED`).
4. **Implement Authoritative Backend Evaluation Function (`evaluate_team_submission`)**:
   - Compares candidate answers against `questions.correct_answer`.
   - Updates `score_r1`, `score_r2`, `total_score`, `accuracy_rate`, and `evaluation_status = 'EVALUATED'`.
5. **Synchronized Event State Control**:
   - Admin "START EVENT" writes `round = '1'`, `round1_start_time`, and `round1_end_time` (+600s).
   - `/api/round/timer` holds candidates in STANDBY until the event is officially active.

---

## 7. Recommended Implementation Order

1. **Phase 1 & 3**: Implement `/api/teams/login` in [server.py](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/server.py) and update [app.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/app.js) to authenticate against the backend.
2. **Phase 4**: Unify Participant Login inside [index.html](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/index.html) (with `login.html` redirecting to `index.html#login`) so fullscreen activated during login is preserved across the entire session.
3. **Phase 6**: Strip answer keys from participant-facing [investigation-data.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/investigation-data.js). Ensure authoritative answer keys reside solely in SQLite.
4. **Phase 7 & 8**: Update [server.py](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/server.py) event control and timer endpoints to enforce synchronized timestamps, pre-event STANDBY states, and automated evaluation calculations.
5. **Phase 9**: Add `/api/violations/log` in [server.py](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/server.py) and wire [app.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/app.js) proctoring listeners to persist violation incidents.
6. **Phase 11**: Add `/api/participant/result` in [server.py](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/server.py) and update [results.html](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/results.html) / [app.js](file:///c:/Users/ADMIN/Documents/TRC%20x%20X/assets/js/app.js) to protect candidate privacy.
7. **Phase 15 & 16**: Perform end-to-end testing, verify all workflows, and generate `CORRECTION_REPORT.md` and `QA_CHECKLIST.md`.
