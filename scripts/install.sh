#!/usr/bin/env bash
set -euo pipefail

repo_url="https://raw.githubusercontent.com/acefolioDev/lean-engineer/main"
target="."
scope="project"
selection=""

usage() {
  cat <<'EOF'
Usage: install.sh [--target DIRECTORY] [--user] [--all]

Installs lean-engineer for Claude Code, Codex, Cursor, and Antigravity.
  --target DIRECTORY  Project directory (default: current directory)
  --user              Install user-level Claude Code, Codex, and Antigravity files
  --all               Install every supported project integration without prompting
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      [[ $# -ge 2 ]] || { echo "--target requires a directory" >&2; exit 2; }
      target="$2"
      shift 2
      ;;
    --user)
      scope="user"
      shift
      ;;
    --all)
      selection="all"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

download() {
  local url="$1"
  local destination="$2"
  mkdir -p "$(dirname "$destination")"
  curl --fail --silent --show-error --location "$url" --output "$destination"
  echo "Installed $destination"
}

if [[ -z "$selection" ]]; then
  if [[ -r /dev/tty ]]; then
    echo "Which coding agent are you using?"
    echo "  1) Codex"
    echo "  2) Claude Code"
    echo "  3) Cursor"
    echo "  4) Antigravity"
    echo "  5) All"
    while true; do
      read -r -p "Choose [1-5]: " selection < /dev/tty
      case "$selection" in
        1) selection="codex"; break ;;
        2) selection="claude"; break ;;
        3) selection="cursor"; break ;;
        4) selection="antigravity"; break ;;
        5) selection="all"; break ;;
        *) echo "Please choose 1, 2, 3, 4, or 5." ;;
      esac
    done
  else
    echo "No interactive terminal found. Re-run with --all or pipe from a terminal." >&2
    exit 2
  fi
fi

if [[ "$scope" == "project" ]]; then
  mkdir -p "$target"
  [[ "$selection" == "claude" || "$selection" == "all" ]] && download "$repo_url/skills/lean-engineer/SKILL.md" "$target/.claude/skills/lean-engineer/SKILL.md"
  [[ "$selection" == "codex" || "$selection" == "all" ]] && download "$repo_url/skills/lean-engineer/SKILL.md" "$target/.agents/skills/lean-engineer/SKILL.md"
  [[ "$selection" == "cursor" || "$selection" == "all" ]] && download "$repo_url/.cursor/rules/lean-engineer.mdc" "$target/.cursor/rules/lean-engineer.mdc"
  [[ "$selection" == "antigravity" || "$selection" == "all" ]] && download "$repo_url/.agents/rules/lean-engineer.md" "$target/.agents/rules/lean-engineer.md"
else
  [[ "$selection" == "claude" || "$selection" == "all" ]] && download "$repo_url/skills/lean-engineer/SKILL.md" "${HOME}/.claude/skills/lean-engineer/SKILL.md"
  [[ "$selection" == "codex" || "$selection" == "all" ]] && download "$repo_url/skills/lean-engineer/SKILL.md" "${HOME}/.agents/skills/lean-engineer/SKILL.md"
  [[ "$selection" == "antigravity" || "$selection" == "all" ]] && download "$repo_url/.agents/rules/lean-engineer.md" "${HOME}/.gemini/config/rules/lean-engineer.md"
fi

echo "lean-engineer installed. Ask your coding agent:"
echo '  Use the lean-engineer skill/rule for this task.'
