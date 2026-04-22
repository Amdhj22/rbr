#!/usr/bin/env bash
# =============================================================================
# Entry point for Tmux Plugin Manager (tpm).
# =============================================================================
#
# tpm locates this file at `~/.tmux/plugins/rbr/rbr.tmux` after cloning
# the repo, runs it as a shell script (it is executable), and we delegate
# to the real theme file under `multiplexers/tmux/` so the monorepo layout
# stays tidy.
#
# Install via tpm (recommended):
#
#     # ~/.tmux.conf
#     set -g @plugin 'tmux-plugins/tpm'
#     set -g @plugin 'Amdhj22/rbr'
#     run '~/.tmux/plugins/tpm/tpm'
#
# Then: prefix + I   (installs all @plugin declarations)
#
# Manual install (without tpm) — source the theme file directly:
#
#     source-file /path/to/multiplexers/tmux/rbr.tmux
#
# =============================================================================

set -eu

PLUGIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" && pwd )"
THEME_FILE="$PLUGIN_DIR/multiplexers/tmux/rbr.tmux"

if [ ! -r "$THEME_FILE" ]; then
  tmux display-message "rbr.tmux: cannot read $THEME_FILE"
  exit 1
fi

tmux source-file "$THEME_FILE"
