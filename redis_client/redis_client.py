import sys
import os

import redis

class RedisClient:
    """Cette classe est la classe redis qui contient les configurations de l'application"""

    def __init__(self):
        self.connect= None

    def connectToServer(self):
        try:
            self.connect = redis.Redis(
                host=os.getenv("REDIS_SERVEUR_HOST"),
                port=os.getenv('REDIS_SERVEUR_PORT'),
                decode_responses=True
            )

            self.connect.client_tracking_on(
                clientid=self.connect.client_id()
            )
            print("Successfull connected to redis server")

        except redis.AuthenticationError:
            print("AuthentificationError on redis client : IA-Decideur")
            raise Exception("AuthentificationError on redis client : IA-Decideur")

    def exist(self,key):
        return True

    def get(self,key):
        return self.connect.get(key)

    def put(self,key,value):
        self.connect.set(key,value)