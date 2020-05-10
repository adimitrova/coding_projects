# ! /usr/bin/env bash
# chmod u+x initial_installs.sh
# sudo ./initial_installs.sh

RED='\e[31m'
GREEN='\e[32m'
NC='\e[0m'
PURPLE_BOLD='\e[35;1m'

cd $HOME
apt update

apps='git zsh python3.5'

for app in $apps;  do 
    apt install $app
    echo ">> ${GREEN}Successfully installed ${PURPLE_BOLD} $app ${NC}"
done

# apt install git
# echo ">> ${GREEN}Successfully installed ${PURPLE_BOLD}git${NC}"