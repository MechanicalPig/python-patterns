import logging


logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self):
        self.subscribers = set()
    
    def register(self, subscriber):
        logger.info('{} registered to {}'.format(subscriber, self))
        self.subscribers.add(subscriber)
    
    def unregister(self, subscriber):
        logger.info('{} unregistered from {}'.format(subscriber, self))
        self.subscribers.remove(subscriber)
    
    def notify(self, msg):
        for subscriber in self.subscribers:
            logger.info('{} notified by {}'.format(subscriber, self))
            subscriber.update(msg)


class Subscriber:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return str(self.name)
    
    def update(self, msg):
        print('{} received: {}'.format(self, msg))


if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO)
    
    publisher = Publisher()
    
    alice = Subscriber('Alice')
    bob = Subscriber('Bob')
    charlie = Subscriber('Charlie')
    
    publisher.register(alice)
    publisher.register(bob)
    publisher.register(charlie)
    
    publisher.notify('Time to wake up!')
    
    publisher.unregister(alice)
    
    publisher.notify('Don\'t tell this to Alice!')
