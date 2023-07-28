import pika


print("Collegamento a RabbitMQ ...")
credentials = pika.PlainCredentials('maurizio', ' @60Runner')
parameters = pika.ConnectionParameters('IT-DESMA01', '27562', '/', credentials)
#myHost="localhost"
#params = pika.ConnectionParameters(myHost)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='worker_queue')

print ("eseguito")

def callback(ch, method, properties,body):
    print ("Ricevuto %s " % body)

channel.basic_consume(  'worker_queue' , callback,True)

channel.start_consuming()

connection.close()
