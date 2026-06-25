#!/bin/bash
# SessionStart hook — provision Python deps so cloud sessions can run the
# inbox-pipeline config tooling and the CapWeb extraction/reconciliation code
# (PDF + Excel parsing) plus lint and tests, with no manual setup.
#
# Synchronous: the session waits until this finishes, so deps are guaranteed
# present before Claude runs anything. Container state is cached after it
# completes, so subsequent sessions start fast.
set -euo pipefail

# Only provision in the remote (Claude Code on the web) environment. Locally
# the user manages their own venv/toolchain.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

echo "[session-start] Installing Python dev dependencies..."
python3 -m pip install --quiet -r requirements-dev.txt

echo "[session-start] Done. Python toolchain ready (parsing libs, ruff, pytest)."
