- [Docker exec command](https://docs.docker.com/engine/reference/commandline/exec/)

Start the docker daemon:
> open --background -a Docker

## Docker initial setup of all requirements and docker compose files to install dependencies and create an image: 
 
https://docs.docker.com/compose/gettingstarted/#step-3-define-services-in-a-compose-file 
1. Create a project folder
2. CD to the project folder
3. Put your code files there for your app
4. Besides the code files, e.g. __app.py__, create also the following files:

- __Dockerfile__ # no extension, just called this way | to create a docker file which will be run and it contains terminal commands to install dependencies and setup default python command to run a certain python file
- __requirements.txt__    # for dependencies
- __docker-compose.yml__      # for adding services

--------------

The Dockerfile is the blueprint for the configuration of an image file. Containers are replicas of the image, based on the same image, but can be configured slightly differently. 

----------------

> docker images    # list avail images
> docker ps -a      # list all (-a) containers that are in post-running or paused condition. 

- If we don't specify the name of the container, it will have an assigned random letters and numbers name by Docker
- Docker assigns each container with a UID which will use to rmeove, start or stop a container
- running `docker run hello-world`, multiple times, there will be multiple replicas of the same image which will be visible after that if we run `docker ps -a` but the image will stay the same and only one.

----------------


To show only __running containers__ use the given command:
> docker ps

To show __all containers__ use the given command:
> docker ps -a

To show the __latest created__ container (includes all states) use the given command:
> docker ps -l

To show __n last created containers__ (includes all states) use the given command:
> docker ps -n=-1

To display __total file sizes__ use the given command:
> docker ps -s

The content presented above is from docker.com.
In the new version of Docker, commands are updated, and some management commands are added:
> docker container ls

Is used to __list all the running__ containers.
> docker container ls -a

Is used to list all the containers created irrespective of its state.

Here container is the management command.

-------------------
