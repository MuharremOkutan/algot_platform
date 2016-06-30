'''Receives data published to "Market" queue and inserts to InfluxDB'''
from influxdb import InfluxDBClient
import pika
import json


def connect_mq(name):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue=name)
	return channel


def connect_db(host='localhost', port=8086, dbname='demodb'):
	user = 'root'
	password = 'root'

	client = InfluxDBClient(host, port, user, password, dbname)
	
	return client


def callback(ch, method, properties, body):
	print(" [x] Received %r...writing to InfluxDB" % json.loads(body))
	data = json.loads(body)
	data['measurement'] = 'cpu_load_short'
	print(data)
	db_conn.write_points(data)
	

if __name__ == '__main__':
	print('Starting InfluxDB tick data recorder...')
	
	channel_name = 'Market'
	conn = connect_mq(channel_name)
	db_conn = connect_db()

	conn.basic_consume(callback,
			   queue=channel_name,
			   no_ack=True)

	print(' [*] Waiting for tick data. To exit press CTR+C')
	conn.start_consuming()



