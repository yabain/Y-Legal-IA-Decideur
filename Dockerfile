FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

# install git
RUN apk --update add bash nano git

# add credentials on build
#RUN mkdir /root/.ssh/
#COPY id_ed25519 /root/.ssh/

#RUN touch /root/.ssh/known_hosts && ssh-keyscan github.com >> /root/.ssh/known_hosts
#RUN git config --global user.name "Cedric-Yaba-In" && git config --global user.email "c.nguendap@yabain.com"

WORKDIR /app

RUN git clone https://github.com/yabain/Y-Legal-IA-Decideur.git .

RUN pip3 install -r requirements.txt

ENV FLASK_APP=main.py

ENV FLASK_DEBUG=0

ENV FLASK_ENV=development

EXPOSE 80

ENTRYPOINT [ "flask","run","--host=0.0.0.0" ]

# CMD ["run", "--host=0.0.0.0"]

# ENTRYPOINT ["python3","app.py"]
