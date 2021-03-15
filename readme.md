# Introduction

This is the github repository for the scientific team project on 'Explainable and Fair Recommendations in Research'. 

# Instructions
Run `python -m pip install -r requirements.txt` to install the requirements. Please note that Gensim requires Visual Studio Code Build Tools, please manually install it before executing the aforementioned command. 

To get the database up and running, use `docker-compose -f ./docker_setup/docker-compose.yaml up` command. Furthermore, you need to load the dataset manually using `apoc load` command.