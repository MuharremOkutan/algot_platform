#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
		'localhost'))

channel = connection.channel()

channel.queue_declare(queue='yahoo_tick')

channel.basic_publish(exchange='',
		      routing_key='yahoo_tick',
		      body='Hello World!')

print(" [x] Sent 'Hello World!'")

connection.close()
