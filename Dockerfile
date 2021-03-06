FROM python:3.8-slim-buster

# install git
RUN apt-get update -y && \
    apt-get install -y git




# add credentials on build
#RUN mkdir /root/.ssh/
#COPY id_ed25519 /root/.ssh/

#RUN touch /root/.ssh/known_hosts && ssh-keyscan github.com >> /root/.ssh/known_hosts
#RUN git config --global user.name "Cedric-Yaba-In" && git config --global user.email "c.nguendap@yabain.com"

WORKDIR /app

RUN git clone https://github.com/yabain/Y-Legal-IA-Decideur.git .

RUN pip install -r requirements.txt

EXPOSE 5000

#ENTRYPOINT [ "flask","run","--host=0.0.0.0" ]

# CMD ["run", "--host=0.0.0.0"]

# CMD ["flask","run"]


