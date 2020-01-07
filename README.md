# datarepo
Data repository and API

## Requirements:

* python 3.8+
* pipenv

## Install Python 3.8+

* Linux users

  * Install "asdf-vm" (version manager): 
  ```
  git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.7.6
  echo -e '\n. $HOME/.asdf/asdf.sh' >> ~/.bashrc
  echo -e '\n. $HOME/.asdf/completions/asdf.bash' >> ~/.bashrc
  asdf update
  ```

  * Install dependencies for asdf plugins: 
  ```
  sudo apt install \
  automake autoconf libreadline-dev \
  libncurses-dev libssl-dev libyaml-dev \
  libxslt-dev libffi-dev libtool unixodbc-dev \
  unzip curl
  ```

  * Install dependencies for Python compilation: 
  ```
  sudo apt update && sudo apt install --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
  ```

  * Add asdf Python plugin and list available versions:
  ```
  asdf plugin-add python
  asdf list-all python
  ```

  * Install choiced Python version (example with 3.8.1):
  ```
  asdf install python 3.8.1
  asdf global python 3.8.1
  ```

## Install pipenv

* Install for local user:
  ```
  python3 -m pip install --user pipenv
  ```

## Run locally

* Clone the repository and run
  ```
  git clone https://github.com/PUG-PB-Traducao/datarepo.git
  cd datarepo
  cp .env.sample .env
  git clone https://github.com/zuarbase/fastapi-sqlalchemy
  pipenv install --dev
  pipenv shell
  docker-compose up -d
  uvicorn main:app --reload
  ```
