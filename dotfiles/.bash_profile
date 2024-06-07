cd {{default_shell_directory}}

# Don't put duplicate lines in the history
export HISTCONTROL=ignoreboth:erasedups

# Set history length
HISTFILESIZE=1000000000
HISTSIZE=1000000

# Append to the history file, don't overwrite it
shopt -s histappend
# Check the window size after each command and, if necessary, update the values of LINES and COLUMNS
shopt -s checkwinsize
# Autocorrect typos in path names when using `cd`
shopt -s cdspell
# Save all lines of a multiple-line command in the same history entry (allows easy re-editing of multi-line commands)
shopt -s cmdhist
# Do not autocomplete when accidentally pressing Tab on an empty line. (It takes forever and yields "Display all 15 gazillion possibilites?")
shopt -s no_empty_cmd_completion

# Do not overwrite files when redirecting using ">". Note that you can still override this with ">|"
set -o noclobber

# Enable some Bash 4 features when possible:
# * `autocd`, e.g. `**/qux` will enter `./foo/bar/baz/qux`
# * Recursive globbing, e.g. `echo **/*.txt`
for option in autocd globstar; do
	shopt -s "$option" 2> /dev/null
done

# Locale
export LC_ALL=en_US.UTF-8
export LANG="en_US"

# Default editor VSCode
export EDITOR="code"

# Load Oh My Posh w/ active theme
eval "$(oh-my-posh init bash --config $OMP_THEME)"

# Add to PATH
export PATH="$PATH:/c/Program Files/Microsoft VS Code/bin:$HOME/.local/bin"