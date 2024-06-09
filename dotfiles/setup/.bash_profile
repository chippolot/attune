load_prompt() {
    if [ -f "{{paths.config}}.env" ]; then . "{{paths.config}}.env"; fi
    eval "$(oh-my-posh init bash --config $OMP_THEME)"
}
attune() {
    initial_omp_theme="$OMP_THEME"
    "{{paths.repo}}/attune.py" "$@"
    if [ -f "{{paths.config}}.env" ]; then . "{{paths.config}}.env"; fi
    if [ "$OMP_THEME" != "$initial_omp_theme" ]; then load_prompt; fi
}
. "{{paths.config}}.bash_profile"
load_prompt