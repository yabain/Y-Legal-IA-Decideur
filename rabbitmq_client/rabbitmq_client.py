import pika

class RabbitMQClient():
    """Cette classe represente la classe rabbitmq client qui permet de faire la communication assynchrone"""
    def __init__(self,config):
        self.connection = None
        self.channel=None
        self.configService=config
        self.onDataCallback={}
        self.config={}

    def getConfiFromConfigService(self):
        self.config.set("rabbitmq_server_host",self.configService.get("rabbitmq_server_host"))
        self.config.set("rabbitmq_server_port",self.configService.get("rabbitmq_server_port"))
        self.config.set("ia_decideur_default_queue_name",self.configService.get("ia_decideur_default_queue_name"))

    def connectoToServer(self):
        self.getConfiFromConfigService()

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.config.get("rabbitmq_server_host"),
                port=self.config.get("rabbitmq_server_port"),
            )
        )
        self.channel=self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.createNewQueue(queueName=self.config.get("ia_decideur_default_queue_name"),exchangeType="direct",routingQueueKey=self.config.get("ia_decideur_default_queue_name"))
        self.channel.start_consuming()

        print("Successfull connected to rabbitmq server")

    def createNewQueue(self,queueName="",handleMessageFct=lambda body:print("Received message ",body),exchangeName="", exchangeType="fanout",routingQueueKey=""):
        queue=self.channel.queue_declare(queue=queueName,durable=True,exclusive=True)

        ##bind between queue and exchange
        self.channel.exchange_declare(exchangeName,exchangeType)
        self.channel.queue_bind( exchange=exchangeName,queue=queue.method.queue,routing_key=routingQueueKey)

        ##declare queue consuming
        self.channel.basic_consume(
            queue=queueName,
            on_message_callback=lambda ch, method, properties, body: self.onReceivedMessage(queueName,ch, method, properties, body,handleMessageFct),
            auto_ack=True,
        )

    def registerOnReceivedDataCallBack(self,queueName,callback):
        if self.onDataCallback.get(queueName) is None:
            self.onDataCallback[queueName]=[]
        self.onDataCallback.get(queueName).append(callback)

    def sendMessage(self,exchange="",routing_key="",data=""):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=data,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

    def onReceivedMessage(self,queueName,ch, method, properties, body,handleMessageFct):
        handleMessageFct(queueName,body,properties)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def closeConnection(self):
        self.connection.close()