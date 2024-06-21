# 🔥 Attune

An opinionated Windows/Mac dev environment setup tool inspired by [@dhh's Omakub](https://github.com/basecamp/omakub).

## 📋 Prerequisites

### 🪟 Windows
* [Python3](https://www.python.org/downloads/)

### 🍎 Mac
* [Python3](https://www.python.org/downloads/)
* [Homebrew](https://brew.sh/)
  * Make sure to follow the post-install steps to add homebrew to your PATH!

## 💿 Installation
1. Clone the Attune repo into any local folder
```
git clone https://github.com/chippolot/attune.git
```
2. Run the `install` shell script in the main repo directory
```
./install
```

## 🚀 Usage

### 🔄 Syncing
```
attune sync
```
Keep Attune and its modules up-to-date with a single command.
This will update the main Attune repo and all installed modules, applying configuration changes in the process.

### 🎨 Themes
```
attune theme
```
Choose from a variety of pre-configured themes to customize your development environment.
Themes will update the system terminal, VSCode, desktop wallpaper, and display mode.

### 🖌️ Fonts
```
attune font
```
Easily switch between programmer-friendly fonts.
Changing the active font will update the font in VSCode and the terminal app.

### 📦 Modules
Attune manages dotfiles, packages, and app extensions via individual modules. A common module comes bundled with Attune and is automatically installed on first launch.

#### Installing Modules
```
attune module install <url>
```
Install modules from a local directory or GitHub repo.

#### Initializing Modules
```
attune module init
```
Create a new module in the current directory with an `.attune-module` folder and a config file.

#### Viewing Modules
```
attune module list
```
List all currently installed modules.

#### Uninstalling Modules
```
attune module uninstall <url>
```
Remove modules from your Attune configuration.

### ⚙️ User Config
```
attune config
```
Open the Attune user config in VSCode to specify the active theme, font, and manage installed modules.

## 🐛 Known Issues
* Installation and syncing may need to be run multiple times due to issues with PATH and other environment variable changes being dependencies for subsequent steps.
* Applying themes on macOS first requires that the user set a static wallpaper which applies to all spaces before the wallpaper command can be run.

## 📜 License
Attune is released under the [MIT License](https://opensource.org/licenses/MIT).
