#!/usr/bin/env bash
# RBR theme applier
# rbr-theme(정본)의 각 도구 테마를 실제 사용 경로(~/.config/*)에 심링크로 배포한다.
# 심링크라 이후 rbr-theme 를 업데이트하면 각 도구에 즉시 반영된다(drift 없음).
#
# 사용: ./scripts/apply.sh [--copy]
#   --copy   심링크 대신 복사본을 배포 (rbr-theme clone 없이도 자립적으로 쓰고 싶을 때)
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}"
MODE="link"
[ "${1:-}" = "--copy" ] && MODE="copy"

log()  { printf "\033[1;34m[rbr]\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m[warn]\033[0m %s\n" "$*"; }

# src(레포 상대경로) → dest(절대경로) 배포
place() {
  local src="$REPO/$1" dest="$2"
  if [ ! -e "$src" ]; then warn "원본 없음, 스킵: $1"; return; fi
  mkdir -p "$(dirname "$dest")"
  if [ "$MODE" = "link" ] && [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    log "ok: $dest"; return
  fi
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    mv "$dest" "${dest}.bak.$$" && warn "기존 백업: ${dest}.bak.$$"
  fi
  if [ "$MODE" = "copy" ]; then
    cp "$src" "$dest"; log "copied: $dest"
  else
    ln -s "$src" "$dest"; log "linked: $dest -> $src"
  fi
}

log "applying RBR from $REPO (mode=$MODE)"

# --- 자동 배포 대상 ---
place "terminals/ghostty/rbr" "$CONFIG/ghostty/themes/rbr"
place "shells/p10k/rbr.zsh"   "$CONFIG/p10k/rbr.zsh"
place "tools/eza/theme.yml"   "$CONFIG/eza/theme.yml"
place "tools/k9s/skin.yaml"   "$CONFIG/k9s/skins/rbr.yaml"

# --- ghostty: 테마 활성화 확인 ---
GCONF="$CONFIG/ghostty/config"
if [ -f "$GCONF" ]; then
  if grep -q '^theme = rbr' "$GCONF"; then
    log "ghostty: theme = rbr 활성화됨"
  else
    warn "ghostty: '$GCONF' 에 'theme = rbr' 를 추가하세요"
  fi
else
  warn "ghostty: 표준 config('$GCONF')가 없습니다."
  warn "  → config.ghostty 를 쓰고 있다면 'config' 로 이름을 바꾸거나 심링크하세요 (안 그러면 로드 안 됨)."
fi

# --- 수동/외부 관리 대상 안내 ---
cat <<EOF

[수동 적용이 필요한 도구]
  • iterm2  : $REPO/terminals/iterm2/RBR.itermcolors 를 Preferences > Profiles > Colors > Import
  • tmux    : TPM 플러그인  set -g @plugin 'Amdhj22/rbr.tmux'   (prefix + I)
  • nvim    : plugin manager 로  Amdhj22/rbr.nvim
  • vscode  : $HOME/workspace/private/rbr.vscode/*.vsix 설치 (code --install-extension)

적용 후 ghostty/tmux/셸을 재시작하면 반영됩니다.
EOF
