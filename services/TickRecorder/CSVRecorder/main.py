'''Receives data published to "Market" queue and inserts to CSV file'''
import pika
import json

def connect_mq(name):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue=name)
	return channel


def write_csv(data):
	pass


def callback(ch, method, properties, body):
	data = json.loads(body)
	print(' [x] Received %r...writing to CSV' % data)
	
	write_csv(data)


if __name__ == '__main__':
	print('Starting CSV tick data recorder...')
	channel_name = 'Market'
	conn = connect_mq(channel_name)

	conn.basic_consume(callback,
			   queue=channel_name,
			   no_ack=True)

	print(' [*] Waiting for tick data. To exit press CTR+C')
	conn.start_consuming()
