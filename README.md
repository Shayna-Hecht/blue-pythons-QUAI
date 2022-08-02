# NLP Project Scaffold!

A scaffold for deploying dockerized flask applications.

If you have any questions, feel free to open an issue on [Github](https://github.com/organization-x/omni/issues).

### Video Guide

[![Deploy a Web Project with Flask](https://img.youtube.com/vi/JUb-PpejA7w/0.jpg)](https://youtu.be/JUb-PpejA7w "Deploy a Web Project with Flask")

This guide covers how you can quickly deploy most projects with the [Flask](https://flask.palletsprojects.com/) framework and our omni scaffold.

### Quickstart Guide for Local Development

cd into the `/app` folder

`python3 -m pip install -r requirements.txt`

You'll want to edit line 96 of the `main.py` file to either the URL of the cocalc server you are on or `localhost` if you are running it on your own PC.

From there, run `python3 -m main` to start the server on local, most changes while developing will be picked up in realtime by the server. Note that upon cloning this repository an example project with an untrained model will show up upon running `python3 -m main`.

### Quickstart Guide for Local Deployment

Make sure docker is installed on your system. Look that up if you don't know what that means.

cd into the root directory of the repo then run 

`docker build -t omni .`

once built, run

`docker run -d -p 9000:80 --restart=unless-stopped --name omni omni`

you should then be able to see the `omni` container running when you run 

`docker ps -a`

if it seems to be stuck (i.e. constantly listed as `Restarting`), something is wrong with the docker image or code inside causing it to repeatedly fail.

you can start debugging the project by running 

`docker logs -f omni` 

or

`docker exec -it omni /bin/bash` for an interactive bash terminal (this option only works if the container is running and not stuck in a restart loop)

### Common Issues

`$'\r': command not found` when attempting to start docker container

this is caused by the the `entrypoint.sh` script somehow having CLRF line endings instead of LF line endings.

to fix this run

`sed -i 's/\r$//' entrypoint.sh`

### File Structure

The files/directories which you will need to edit are **bolded**, and the files you **may** need to edit are *italicized*.

**DO NOT TOUCH OTHER FILES. THIS MAY RESULT IN YOUR PROJECT BEING UNABLE TO RUN**

- .gitignore
- config.py
- Dockerfile
- READMD.md
- entrypoint.sh
- nginx_host
- host_config
- app/
     - **main.py**
     - *requirements.txt*
     - **utils.py**
     - templates/
          - **writer_home.html**
          - **Write-your-story-with-AI.html**
     - static/
          - **img/** 
          - **js/**
          - **css/**
          - favicon.ico  
     - model/
          - **TODO.txt** <- delete this file after following the directions. Important to note that you will only need an aitextgen.tokenizer.json file if you are custom training your own tokenizer and model.

### main.py ###

Contains the main flask app itself. Currently the model in use is an untuned GPT-NEO model. You are going to want to comment out the snippet `ai = aitextgen(model_folder="model/", tokenizer_file="model/aitextgen.tokenizer.json", to_gpu=False)` to load in your model once you have put the appropriate files in the `model/` folder. If you do not have a tokenizer file, delete the second argument of the function. 

### requirements.txt ###

Contains list of packages and modules required to run the flask app. Edit only if you are using additional packages that need to be pip installed in order to run the project.

To generate a requirements.txt file you can run

`pip list --format=freeze > app/requirements.txt`

the requirements.txt file will then be updated. Keep in mind: some packages you install on one operating system may not be available on another. You will have to debug and resolve this yourself if this is the case.

### utils.py ###

Contains common functions used by the flask app. Put things here that are used more than once in the flask app.

### templates/ ###

Contains the HTML pages used for the webpage. Edit these to fit your project. The pages `writer_home.html` and `Write-your-story-with-AI.html` are from the example project and should be referenced when building your bootstrap site!

### static/ ###

Contains the static images, CSS, & JS files used by the flask app for the webpage. You will need to put your css and js files in it. Place all your images used for your website in static/img/ so that you can then reference them in your html files.

### model/ ###

Contains all necessary information to load in your model to aitextgen. Place your config.json, pytorch_model.bin, and aitextgen.tokenizer.json(if applicable) files in this folder. You are going to want to comment out the snippet `ai = aitextgen(model_folder="model/", tokenizer_file="model/aitextgen.tokenizer.json", to_gpu=False)` in main once you have done this.

### Files used for deployment ###

`config.py`
`Dockerfile`
`entrypoint.sh`
`nginx_host`
`host_config`
**Only modify `host_config`. Do not touch the other files.**

