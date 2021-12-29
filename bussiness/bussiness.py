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

    def connectToServers(self):
        try:
            self.config.connect()
            self.rabbitmq.connection()
        except Exception:
            sys.exit(-1)

    def predict(self,text):
        return self.classifier.predict(self.pretraitedText.removeReturnLine(text))

    def predictFromTextStream(self,stream):
        prediction= self.predict(readTextFromPDFDoc(readPDFFromStream(stream)))

        if prediction:
            self.rabbitmq.sendMessage(self.exchangename,routing_key=self.routingKey,data=stream)
        return prediction
