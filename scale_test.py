import logging
from client_test import ScaleTest

log = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    url = "https://twitter-alb-1269535057.us-west-2.elb.amazonaws.com"
    # url = "http://localhost:11222"
    test = ScaleTest(url)
    test.test()
