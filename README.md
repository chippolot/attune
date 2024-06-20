# Attune
An opinionated Windows/Mac dev environment setup tool inspired by [@dhh's Omakub](https://github.com/basecamp/omakub).

## Prereqs
### Windows
* [Python3](https://www.python.org/downloads/)
### Mac
* [Homebrew](https://brew.sh/)
    * Make sure that your PATH has been updated after installing homebrew (instructions can be found in installation output.)
* [Python3](https://www.python.org/downloads/)

## Installation
To install, simply clone the attune repo into any local folder and then run the `install` shell script.

## Usage
* `attune sync`<br/>
Syncs the attune git repo and applies any changes.

* `attune theme`<br/>
Shows the theme select menu. Selecting a theme will update the system terminal, VSCode, the desktop wallpaper, and the system display mode (light mode / dark mode).

* `attune font`<br/>
Shows the font select menu. Selecting a font will update the font in the system terminal and VSCode.

* `attune config`<br/>
Opens the attune user config in VSCode.

## Known Issues
* Installation and syncing may need to be run multiple times due to issues with PATH and other environment variable changes being dependencies for subsequent steps.

## License
Attune is released under the [MIT License](https://opensource.org/licenses/MIT).
