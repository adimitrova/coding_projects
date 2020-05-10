FROM python:3.5-slim

ENV HOMEDIR /home/epubify

# Create a new system user
RUN useradd -ms /bin/bash epuser
USER epuser

# Set the container working directory to the user home folder
#   WORKDIR /home/epubify
WORKDIR ${HOMEDIR}

ADD epubify.py ${HOMEDIR}
ADD requirements.txt ${HOMEDIR}

# RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y python3 python3-pip \
    && pip3 install -r ${HOMEDIR}/requirements.txt

CMD [ "python3", "/epubify.py" ]