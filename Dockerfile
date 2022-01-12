FROM ubuntu as intermediate

# install git
RUN apt-get update
RUN apt-get install -y git

# add credentials on build
RUN mkdir /root/.ssh/
COPY id_ed25519 /root/.ssh/

RUN touch /root/.ssh/known_hosts && ssh-keyscan github.com >> /root/.ssh/known_hosts
RUN git config --global user.name "Cedric-Yaba-In" && git config --global user.email "c.nguendap@yabain.com"

RUN git clone https://github.com/yabain/Y-Legal-IA-Decideur.git /app






FROM python:3

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev 

COPY --from=intermediate /app /app
RUN cd /app && pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["main.py"]
