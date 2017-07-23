#!/bin/bash

USERNAME=$(whoami)
INSTALL_DIR=$(pwd)

# Get superuser privileges
#
# Install basic applications
#
# Git
# sudo -i apt-get install git
#
# Neovim
# sudo add-apt-repository ppa:neovim-ppa/stable
# sudo apt-get update
# sudo apt-get install neovim
#
# Zsh
# sudo apt-get install zsh
# chsh -s $(which zsh)
#
# Oh-my-zsh
# sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
#
# Curl
# sudo apt-get install curl
#
# Copy .zshrc to home directory
# cp ./config_files/.zshrc ~/.zshrc
#
# Install compilers (bazel and g++)
# sudo apt-get install g++
#echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
#curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
#sudo apt-get update && sudo apt-get install bazel
#bazel
#
# Install OpenCV
#sudo apt-get install build-essential
#sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
#
#git clone https://github.com/opencv/opencv ~/third_party/opencv
#
#cd ~/third_party/opencv
#mkdir cmake_binary_dir
#cd cmake_binary_dir
#
# Use cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/usr/local .. , without spaces after -D if this command does not work.
#cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
#make
#sudo make install
#
#cd $INSTALL_DIR
#
## Install PortAudio
#sudo apt-get install libasound-dev
#PA_VERSION="pa_stable_v190600_20161030.tgz"
#wget http://www.portaudio.com/archives/$PA_VERSION
#mkdir ~/third_party/portaudio/
#tar -xvzf $PA_VERSION -C ~/third_party/
#rm $PA_VERSION
#
#cd ~/third_party/portaudio/
#chmod 777 ./configure
#./configure && make
#sudo make install
#
cd $INSTALL_DIR
sudo apt-get install v4l-utils
