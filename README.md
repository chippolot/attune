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
### Syncing
Attune has the ability to update itself if it has been cloned directly from GitHub. Running `attune sync` will update the main attune repo as well as any modules which have been installed from git urls.
After updating, syncing applies core attune configuration changes as well as changes associated with all installed modules.

### Themes
Attune comes with several pre-configured themes. Themes update the system terminal, VSCode, the desktop wallpaper, and the system display mode (light mode / dark mode).
Running the `attune theme` command shows a theme picker which can be used to set the active system theme.

### Fonts
* `attune font`<br/>
Attune comes bundled with a font config which downloads several programmer-friendly fonts. Changing the active font will update the font in VSCode and the terminal app.
Running the `attune font` command shows a font picker which can be used to set the active font.

### Modules
Attune manages dotfiles, packages, and app extensions via individual modules. A common module currently comes bundled with attune which is automatically installed on first launch.

#### Installing New Modules
Modules can be installed from either a local directory or a github repo.
Running `attune module install <url>` will register a local or remote module with your attune config and apply it immediately.
For local modules, the `url` is the full local path to the folder containing the `.attune-module` folder.
For remote modules, the `url` is the url of the github repo containing an `.attune-module` folder.

#### Viewing Installed Modules
Running `attune module list` will list all currently installed modules.

#### Uninstalling Modules
Modules can be uninstalled by running `attune module uninstall <url>`.

#### Creating Your Own Modules
Create a new module by running `attune module init` from any folder. Running this command creates an `.attune-module` folder in the current directory and initializes a config file w/ several optional dotfile extensions.
You can initialize an empty github repo and push the changes to start a new remote module.

### User Config
`attune config`<br/>
Opens the attune user config in VSCode. User config specfies the active theme, font, and contains a manifest of installed modules.

## Known Issues
* Installation and syncing may need to be run multiple times due to issues with PATH and other environment variable changes being dependencies for subsequent steps.
* Applying themes on MacOS first requires that the user set a static wallpaper which applies to all spaces before the wallpaper command can be run.

## License
Attune is released under the [MIT License](https://opensource.org/licenses/MIT).
