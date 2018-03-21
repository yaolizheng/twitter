import logging
from client_test import FunctionalTest


log = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    url = "https://twitter-alb-1269535057.us-west-2.elb.amazonaws.com"
    # url = "http://localhost:11222"
    test = FunctionalTest(url)
    test.test()
