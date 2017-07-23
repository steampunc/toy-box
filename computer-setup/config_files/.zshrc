# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH=/home/finn/.oh-my-zsh

# Set terminal to more than 256 colors
export TERM="xterm-256color"

# Most of this is stolen from https://github.com/bhilburn/powerlevel9k/wiki/Show-Off-Your-Config#rjorgensons-configuration

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="geometry/geometry"

# Enable command auto-correction.
ENABLE_CORRECTION="true"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git)

source $ZSH/oh-my-zsh.sh

eval `dircolors ~/.config/.dircolors`

alias bz='bazel'
alias vim='nvim'

export VISUAL=nvim
export EDITOR="$VISUAL"

weather() {
  sh -c "curl http://wttr.in/Davis"
}

