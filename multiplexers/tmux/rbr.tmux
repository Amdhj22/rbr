# =============================================================================
# RBR — Red Bull Racing theme for tmux
# Version: 2.1.0-classic
# =============================================================================
#
# Inspired by the Red Bull Racing F1 livery:
#   - Active pane border  : kerb red   (#e84a55) — "which pane owns focus"
#   - Active window tab   : kerb red   — "which window you're on"
#   - Session name badge  : RB yellow  (#ffd84d) — "which session this is"
#   - Messages / prompts  : RB yellow  — attention color
#   - Clock mode          : kerb red
#
# Install:
#   1. Copy this file somewhere (e.g. ~/.config/tmux/rbr.tmux)
#   2. In ~/.tmux.conf add:
#        source-file ~/.config/tmux/rbr.tmux
#   3. Reload:  tmux source-file ~/.tmux.conf
#
# Requires: tmux 3.0+ (hex colors) and a true-color terminal
#           (`set -g default-terminal "tmux-256color"` +
#            `set -ag terminal-overrides ",*:RGB"`)
# =============================================================================

# ---- Pane borders -----------------------------------------------------------
# Inactive = muted overlay; active = kerb red (the one thing that's focused).
set -g pane-border-style        'fg=#3a4466'
set -g pane-active-border-style 'fg=#e84a55'

# ---- Status bar -------------------------------------------------------------
set -g status           'on'
set -g status-position  bottom
set -g status-justify   centre
set -g status-interval  5
set -g status-style     'fg=#c8d0e8,bg=#070d1f'    # text on mantle

# ---- Status left: session badge + hostname ---------------------------------
# Session name is the one thing you always want to know — RB yellow badge.
set -g status-left-length 60
set -g status-left '#[fg=#0a1128,bg=#ffd84d,bold] #S #[fg=#ffd84d,bg=#15203f,nobold]#[fg=#c8d0e8,bg=#15203f]  #h #[fg=#15203f,bg=#070d1f] '

# ---- Status right: clock + date --------------------------------------------
set -g status-right-length 60
set -g status-right '#[fg=#15203f,bg=#070d1f]#[fg=#c8d0e8,bg=#15203f]  %H:%M #[fg=#ffd84d,bg=#15203f]#[fg=#0a1128,bg=#ffd84d,bold] %d %b '

# ---- Window tabs ------------------------------------------------------------
# Inactive tabs recede; active tab claims the kerb-red spotlight.
setw -g window-status-format         '#[fg=#8590ae,bg=#070d1f]  #I  #W  '
setw -g window-status-current-format '#[fg=#070d1f,bg=#e84a55]#[fg=#0a1128,bg=#e84a55,bold]  #I  #W  #[fg=#e84a55,bg=#070d1f]'
setw -g window-status-separator      ''

# Activity / bell badges on inactive windows.
setw -g window-status-activity-style 'fg=#ffd84d,bg=#070d1f,bold'
setw -g window-status-bell-style     'fg=#0a1128,bg=#f56570,bold'
setw -g window-status-last-style     'fg=#c8d0e8,bg=#070d1f'

# ---- Messages & prompts -----------------------------------------------------
# Messages (`tmux display-message`) and the command prompt both use RB yellow —
# they are "attention now" interactions, same as the editor cursor.
set -g message-style         'fg=#0a1128,bg=#ffd84d,bold'
set -g message-command-style 'fg=#0a1128,bg=#f5c842,bold'

# ---- Copy mode (visual selection) -------------------------------------------
set -g mode-style 'fg=#0a1128,bg=#ffd84d'

# ---- Clock mode (prefix + t) ------------------------------------------------
set -g clock-mode-colour '#e84a55'
set -g clock-mode-style  24
