import pika
import sys

print("Collegamento a RabbitMQ ...")


#config.get('rabbitmq')['user'], config.get('rabbitmq')['password'])

credentials = pika.PlainCredentials('maurizio', ' @60Runner')
parameters = pika.ConnectionParameters('IT-DESMA01', '25672', '/', credentials)

#credentials = pika.PlainCredentials(host = 'rabbit@IT-DESMA01')
#params = pika.ConnectionParameters("localhost")


connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='worker_queue')

print ("eseguito")

i=0
while True:
    message=str(i)
    i +=1
    channel.basic_publish(exchange='', routing_key='worker_queue', body=message)
    print("Inviato messaggi %s", message)
    if (i > 100000):
        break

connection.close()
sys.exit()

