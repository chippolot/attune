# Append to the history file, don't overwrite it
setopt APPEND_HISTORY
# Autocorrect typos in path names when using `cd`
setopt CORRECT
# Save all lines of a multiple-line command in the same history entry (allows easy re-editing of multi-line commands)
setopt HIST_IGNORE_ALL_DUPS
# Do not autocomplete when accidentally pressing Tab on an empty line.
setopt NO_AUTO_MENU

# Do not overwrite files when redirecting using ">". Note that you can still override this with ">|"
setopt NO_CLOBBER

# Enable some Bash-like features:
# * `autocd`, e.g. `**/qux` will enter `./foo/bar/baz/qux`
# * Recursive globbing, e.g. `echo **/*.txt`
setopt AUTO_CD
setopt GLOBSTAR_SHORT

# Additional settings specific to zsh history management
setopt SHARE_HISTORY       # Share history across multiple zsh sessions
setopt HIST_IGNORE_DUPS    # Don't record an entry that was just recorded again
setopt HIST_REDUCE_BLANKS  # Remove superfluous blanks before recording entry

# Disable terminal sounds
unsetopt BEEP