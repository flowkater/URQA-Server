import sys
import pika

credentials = pika.PlainCredentials('guest', 'guest')
parameters  = pika.ConnectionParameters(host='14.63.164.245', 
                                        port=5672, 
                                        credentials=credentials)

connection  = pika.BlockingConnection(parameters)
channel     = connection.channel()

channel.exchange_declare(exchange='ur-exchange', type='fanout')
result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue
print queue_name

channel.queue_bind(exchange ='ur-exchange', queue = queue_name)

print " [*] Waiting for messages. To exit press CTRL+C"
#logger.info(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print " [x] Received %r\n\n" % (body,)

'''
    try:
        data = json.loads(body)
    except (ValueError):
        print 'JSON TypeError'
        #logger.error('JSON TypeError')
        return

    fields = ['receivers', 'data'];
    result = filter(lambda x: x in data, fields)
    if len(result) != len(fields):
        print 'Get off'
        #logger.error('Get off')
        return

    receivers = data['receivers']
    message   = data['data']
    ostype    = data['os']

    if type(receivers) is not list:
        print 'Invalid receivers'
        #logger.error('Invalid receivers')
        return
'''

if __name__ == '__main__':
    try:
        channel.basic_consume(callback, queue=queue_name, no_ack=True)
        channel.start_consuming()
    except (KeyboardInterrupt):#, SystemExit):
        #logger.debug('Program Exit....\n')
	channel.stop_consuming()
    connection.close()
    sys.exit(1)

