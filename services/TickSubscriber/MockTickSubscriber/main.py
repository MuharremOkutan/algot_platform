'''Simulates receiving tick data from a broker's API and will publish this to the market queue'''
import time
import random
import pika
import json
import datetime
import pandas as pd

###############################
# TO DO
# 1. Send dict of data (time, bid, ask, last, pair, broker)
##############################

def connect(name):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.queue_declare(queue=name)
	return channel


if __name__ == '__main__':
	channel_name = 'Market'
	conn = connect(channel_name)

	heart_beat = 25
	base_price = 100
        max_iter = 10
	i = 0
	print('Starting Mock Data Tick Subscriber...')
      	
	while i < max_iter:
		
		price = base_price + random.randint((base_price*.1)*-1,(base_price*.1))
		l = {"Time": datetime.datetime.today().strftime('%Y-%m-%d'),
		     "Price": price
		     }
		print('Publishing mock tick data...')
		conn.basic_publish(exchange='',
				   routing_key=channel_name,
				   body=json.dumps(l))
		print(' [x] Sent %d', price)
		i += 1
		time.sleep(heart_beat)
	
	conn.close()
