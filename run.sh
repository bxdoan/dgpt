#!/bin/sh

doc_str="Usage: ./run.sh [file_name] [arguments]
    example: ./run.sh
"
# pull latest code
git pull

mkdir -p log
mkdir -p tmp

file_name=${pf##*/}
today=$(date '+%Y-%m-%d_%H:%M:%S')
file_name_log="log/${file_name%.*}_${today}.log"

# set pipenv path
if [[ -f "$HOME/.pyenv/shims/pipenv" ]]; then
  pipenv="$HOME/.pyenv/shims/pipenv"
elif [[ -f "$HOME/.local/bin/pipenv" ]]; then
  pipenv="$HOME/.local/bin/pipenv"
elif [[ -f "/opt/homebrew/bin/pipenv" ]]; then
  pipenv="/opt/homebrew/bin/pipenv"
elif [[ -f "/usr/local/bin/pipenv" ]]; then
  pipenv="/usr/local/bin/pipenv"
else
  echo "pipenv application not found"
fi

$pipenv sync

echo "Running $pf with arguments $@\n"
PYTHONPATH=`pwd` $pipenv run python src/chat.py 2>&1
cat $file_name_log
echo "check file $file_name_log"