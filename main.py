def run(config):
    import logging
    import logging.config
    if "logging" in config:
        logging.config.dictConfig(config['logging'])
    else:
        logging.basicConfig(level=logging.DEBUG, format=(
            "%(levelname)s %(asctime)s name={name} "
            "process=%(process)d thread=%(thread)d "
            "(%(module)s) %(message).10000s".format(name=config["node"])
        ))
    log = logging.getLogger(__name__)
    try:
        return _run(config)
    except:
        log.exception(__name__)
        raise


def _run(config):
    import http_server
    webserver = http_server.WebServer(config)
    webserver.serve()
