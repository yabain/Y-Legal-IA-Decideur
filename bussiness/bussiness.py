import sys

from bussiness.classifier.text_lois_classifier import TextLoiClassifier
from rabbitmq_client.rabbitmq_client import RabbitMQClient
from redis_client.redis_client import RedisClient
from utils.pdf import readTextFromPDFDoc, readPDFFromStream, PreTraitedText


class BussinessClassifier:
    def __init__(self):
        self.pretraitedText = PreTraitedText()
        self.classifier = TextLoiClassifier()
        self.config = RedisClient()
        self.rabbitmq = RabbitMQClient(self.config)

        self.connectToServers()

        self.exchangename=self.config.get("ia_bussiness_get_posted_valid_document_queue_name")
        self.routingKey = self.config.get("ia_bussiness_get_posted_valid_document_routing_key")

        print("end bussiness")


    def startRabbimtMQ(self):
        self.rabbitmq.startConsuming()
    def connectToServers(self):
        try:
            self.config.connectToServer()
            print("end rabbit")
            self.rabbitmq.getConfiFromConfigService()
            self.rabbitmq.connectoToServer()

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            print(err)
            sys.exit(-1)

    def predict(self,text):
        return self.classifier.predict(text)

    def predictFromTextStream(self,stream):
        text = self.pretraitedText.removeReturnLine(readTextFromPDFDoc(readPDFFromStream(stream)))
        prediction= self.predict(text)

        #if prediction:
        #    self.rabbitmq.sendMessage(self.exchangename,routing_key=self.routingKey,data=stream)

        self.rabbitmq.sendMessage('y_legal',self.config.get("indexeur_default_queue_name"),text)
        return prediction
