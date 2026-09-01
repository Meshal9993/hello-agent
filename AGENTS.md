# Project rules

- Keep the backend in `backend/` and the frontend in `frontend/`.
- Use FastAPI for backend HTTP APIs and Vue for the frontend UI.
- Do not install or upgrade dependencies unless the task explicitly requests it.
- Keep configuration and documentation current when adding tooling or application entry points.
- Prefer focused, well-tested changes; do not alter unrelated files.

## AutoLoop macro

**Trigger:** `AutoLoop`

Perform a bounded fix-and-verify loop.

1. Read `AGENTS.md`, `README.md`, and the relevant verification instructions.
2. State the acceptance check for the current task.
3. Run the smallest relevant check.
4. If the check fails for an in-scope source-code reason, inspect the evidence, make the smallest relevant correction, and rerun the check.
5. Repeat for no more than five correction cycles.
6. Stop early and ask for direction if the next action requires a dependency change, machine-level permission, destructive action, an unrelated process to be stopped, or broader scope.
7. Report every cycle, the final evidence, and anything not verified.

## SmokeTest macro

**Trigger:** `Run the smoke test`

Verify the working application without changing source code or dependency declarations.

1. Read `AGENTS.md`, `README.md`, and `docs/verification.md`.
2. Run the backend pytest suite.
3. Run the frontend lint and production build.
4. Check the intended backend and frontend ports. Never stop an unrelated process.
5. Start only the backend and frontend processes needed for this test in Codex-managed terminals.
6. Verify one successful API request and division-by-zero handling.
7. Use automated browser control to operate the visible calculator. Enter 7 and 6, multiply them, and confirm that the displayed result is 42.
8. Confirm that the browser displays no application error and report any UI behavior that could not be tested.
9. Unless asked to keep the app running, stop only the processes created by this smoke test.
10. Report concise evidence from tests, builds, endpoints, the automated UI interaction, and service cleanup.

## Combined trigger

**Trigger:** `AutoLoop: run the smoke test`

Run the SmokeTest macro. If an in-scope check fails, use the AutoLoop rules to make the smallest correction and repeat the smoke test until it passes, five correction cycles are exhausted, or a stopping condition is reached.
