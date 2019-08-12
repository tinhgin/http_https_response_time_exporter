from prometheus_client import start_http_server, Gauge, CollectorRegistry, push_to_gateway
import logging, time, sys, os, requests
import numpy as np

logger = logging.getLogger('RESP_TIME_EXPORTER')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
registry = CollectorRegistry()
g = Gauge('resp_time', 'Response time', registry=registry)


def total_seconds(timedelta):
    try:
        seconds = timedelta.total_seconds()
    except AttributeError:
        one_second = np.timedelta64(1000000000, 'ns')
        seconds = timedelta / one_second
    return seconds


def get_resp_time(url):
    resp = requests.get(url)
    resp_time = total_seconds(resp.elapsed)*1000
    logger.info("Resp_time for %s : %s ms"  % (url, resp_time))
    return resp_time


if __name__ == '__main__':
    try:
        sleeptime = int(os.environ['INTERVAL'])
        logger.info("Environment variable INTERVAL=%s" % sleeptime)
    except:
        sleeptime = 10
        logger.debug("Environment variable INTERVAL is not set. Use default INTERVAL=%s" % sleeptime)

    try:
        url = os.environ['URL']
        logger.info("Environment variable URL=%s" % url)
    except:
        url = "http://127.0.0.1"
        logger.debug("Environment variable URL is not set. Use default URL=%s" % url)

    try:
        pushgateway = os.environ['PUSHGATEWAY']
        logger.info("Environment variable PUSHGATEWAY=%s" % pushgateway)
    except:
        pushgateway = "http://127.0.0.1"
        logger.debug("Environment variable PUSHGATEWAY is not set. Use default PUSHGATEWAY=%s" % pushgateway)

    try:
        dockerservice = os.environ['DOCKERSERVICE']
        logger.info("Environment variable DOCKERSERVICE=%s" % dockerservice)
    except:
        dockerservice = "unknown_dockerservice"
        logger.debug("Environment variable DOCKERSERVICE is not set. Use default DOCKERSERVICE=%s" % dockerservice)

    # Start up the server to expose the metrics.
    #start_http_server(8000)

    while True:
        try:
            g.set(get_resp_time(url))
        except Exception as e:
            logger.error(url + " %s" % e)
            sys.exit(1)
        try:
            push_to_gateway(pushgateway, job=dockerservice, registry=registry)
        except Exception as e:
            logger.error(e)
            sys.exit(1)

        time.sleep(sleeptime)
