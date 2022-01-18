FROM python:3

# install git
RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    apt-get install -y git

# add credentials on build
#RUN mkdir /root/.ssh/
#COPY id_ed25519 /root/.ssh/

#RUN touch /root/.ssh/known_hosts && ssh-keyscan github.com >> /root/.ssh/known_hosts
#RUN git config --global user.name "Cedric-Yaba-In" && git config --global user.email "c.nguendap@yabain.com"

WORKDIR /app

RUN git clone https://github.com/yabain/Y-Legal-IA-Decideur.git .

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["main.py"]


