import logging


logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self):
        self.subscribers = dict()
    
    def register(self, subscriber, callback):
        logger.info('{} registered function {} to {}'.format(
            subscriber, callback.__name__, self))
        self.subscribers[subscriber] = callback
    
    def unregister(self, subscriber):
        logger.info('{} unregistered from {}'.format(subscriber, self))
        del self.subscribers[subscriber]
    
    def notify(self, *args, **kargs):
        for subscriber, callback in self.subscribers.items():
            logger.info('{} notified by {}'.format(subscriber, self))
            callback(*args, **kargs)


def external_function(*args, **kargs):
    print('I\'m a function')


class SubscriberOne:
    def __init__(self, name, pub):
        self.name = name
        pub.register(self, self.method_callback)
    
    def __str__(self):
        return str(self.name)
        
    def method_callback(self, *args, **kargs):
        print('{} notified with {} args and {} kargs'.format(
            self, len(args), len(kargs)))


class SubscriberTwo:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return str(self.name)


if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO)
    
    publisher = Publisher()
    
    # the registration is done via object initialization
    alice = SubscriberOne('Alice', publisher)
    
    # we register an external function as callback
    bob = SubscriberTwo('Bob')
    publisher.register(bob, external_function)
    
    publisher.notify('Time to wake up!')
    publisher.notify('msg', arg1=1, arg2=2)
    
    publisher.unregister(alice)
    
    publisher.notify('Don\'t tell this to Alice!')
