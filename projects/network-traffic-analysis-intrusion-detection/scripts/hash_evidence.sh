#!/usr/bin/env bash
set -euo pipefail
TARGET_DIR="${1:-evidence}"
if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Directory not found: $TARGET_DIR" >&2
  exit 1
fi
MANIFEST="$TARGET_DIR/SHA256SUMS.txt"
# Avoid hashing the manifest into itself.
find "$TARGET_DIR" -type f ! -name "$(basename "$MANIFEST")" -print0 \
  | sort -z \
  | xargs -0 -r sha256sum > "$MANIFEST"
echo "[+] Wrote integrity manifest: $MANIFEST"
