## Initial setup of Macbook:
__[1]__ Download [__iTerm2__](https://www.iterm2.com/) and install it: it's a replacement for the regular terminal. Gives a ton of cool features, such as:
- `Tab`: autocomplete for folders and files and preview of what's in the current location while doing `cd`
- Open multiple sub-windows in the same window
    - `Command + D`: Vertical split, e.g. one window left and one right
    - `Command + Shift + D`: Horizontal split, e.g. one up and one down.

------------------

__[2]__ Install ZShell (zsh). Run:
```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```
- Other [zsh installation options](https://github.com/robbyrussell/oh-my-zsh/wiki/Installing-ZSH)

To make zsh be the default shell, in `iTerm > Preferences > Profiles > Command > Command`, add `/bin/zsh -l`

Default config file for it is located at `~/.zshrc`, and contains a section, called `plugins`. If working with kubernetes, docker and github, add these to the plugins section:
```bash
plugins=(
    git 
    zsh-syntax-highlighting 
    zsh-autosuggestions
    colorize
    brew
    docker 
    kubectl 
    minikube
    pip 
    python 
    sudo 
    osx 
    encode64
)
```    

`kubectl` gives a ton of useful kubernetes shortcuts, see them [__HERE__](https://github.com/robbyrussell/oh-my-zsh/tree/master/plugins/kubectl). 
- A list of many many cool plugins and instructions can be found [__HERE__](https://github.com/unixorn/awesome-zsh-plugins).

------------------

__[3]__ Install the cool [Powerlevel9k](https://github.com/bhilburn/powerlevel9k) theme, which is highly customizable. Here are some useful readings on that:
- How to [display the currently activated virtualenv for python](https://medium.com/@ryanwhocodes/hi-mebin-yes-there-is-5d474766b1ea)
- [Show off your custom config](https://github.com/bhilburn/powerlevel9k/wiki/Show-Off-Your-Config)
- [Awesome font for terminal](https://github.com/gabrielelana/awesome-terminal-fonts/wiki/OS-X)
- [Check a font you've downloaded](https://bluejamesbond.github.io/CharacterMap/) and get the unicode code to use in the theme

My theme:
![iterm2](iterm2_zsh_powerlevel9k.png)

My custom config:

```bash
ZSH_THEME="powerlevel9k/powerlevel9k"

POWERLEVEL9K_MODE='nerdfont-complete'

# Customise the Powerlevel9k prompts
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  #dir
  dir_joined
  #custom_python
  #context
  vcs
  newline
  virtualenv
  #kubecontext
  #docker_machine
  #status
)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(
  aws
  battery
  time
)
POWERLEVEL9K_PROMPT_ADD_NEWLINE=false

## Create a custom Python prompt section
POWERLEVEL9K_CUSTOM_PYTHON="echo -n '\uf81f' Python"
POWERLEVEL9K_CUSTOM_PYTHON_FOREGROUND="black"
POWERLEVEL9K_CUSTOM_PYTHON_BACKGROUND="blue"

POWERLEVEL9K_VCS_MODIFIED_FOREGROUND='196'
POWERLEVEL9K_VCS_MODIFIED_BACKGROUND='239'
POWERLEVEL9K_VCS_CLEAN_FOREGROUND='046'
POWERLEVEL9K_VCS_CLEAN_BACKGROUND='239'
POWERLEVEL9K_VCS_UNTRACKED_FOREGROUND='226'
POWERLEVEL9K_VCS_UNTRACKED_BACKGROUND='239'

#POWERLEVEL9K_BATTERY_UNTRACKED_BACKGROUND='239'
#POWERLEVEL9K_BATTERY_UNTRACKED_FOREGROUND='black'
POWERLEVEL9K_BATTERY_VERBOSE=false
#POWERLEVEL9K_BATTERY_STAGES="▁▂▃▄▅▆▇█"
POWERLEVEL9K_BATTERY_STAGES=''
POWERLEVEL9K_BATTERY_LEVEL_BACKGROUND=(red1 orangered1 darkorange orange1 gold1 yellow1 yellow2 greenyellow chartreuse1 chartreuse2 green1)
POWERLEVEL9K_BATTERY_LOW_FOREGROUND='black'
POWERLEVEL9K_BATTERY_CHARGING_FOREGROUND='black'
POWERLEVEL9K_BATTERY_CHARGED_FOREGROUND='black'
POWERLEVEL9K_BATTERY_DISCONNECTED_FOREGROUND='black'

POWERLEVEL9K_DIR_HOME_BACKGROUND='030'
POWERLEVEL9K_DIR_HOME_SUBFOLDER_BACKGROUND='030'
POWERLEVEL9K_DIR_ETC_BACKGROUND='030'
POWERLEVEL9K_DIR_DEFAULT_BACKGROUND='030'
POWERLEVEL9K_DIR_HOME_FOREGROUND='230'
POWERLEVEL9K_DIR_HOME_SUBFOLDER_FOREGROUND='230'
POWERLEVEL9K_DIR_ETC_FOREGROUND='230'
POWERLEVEL9K_DIR_DEFAULT_FOREGROUND='230'

POWERLEVEL9K_TIME_BACKGROUND='030'
POWERLEVEL9K_TIME_FOREGROUND='230'

POWERLEVEL9K_VIRTUALENV_BACKGROUND='226'
POWERLEVEL9K_VIRTUALENV_FOREGROUND='239'
```

------------------

__[4]__ Colours and other cool stuff with `VIM`

Modify the `~/.vimrc` file in your home directory with the following:

```shell
set number
set ignorecase
set smartcase
syntax enable

" set indentation to 4 spaces
set tabstop=4

" automatically indent with the same nr of tabs like the line above
" set autoindent
set cursorline

" show current file name, being modified
set title

" set undo limit to 1000
set history=1000

" ednable spell check
" set spell
```