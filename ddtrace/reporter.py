"""
Report spans to the Agent API.
"""
import logging
from time import time

# project
from .transport import ThreadedHTTPTransport
from .encoding import encode_spans, encode_services


log = logging.getLogger(__name__)


class AgentReporter(object):

    SERVICES_FLUSH_INTERVAL = 120

    def __init__(self, hostname, port):
        self.transport = ThreadedHTTPTransport(hostname, port)
        self.last_services_flush = 0

    def report(self, spans, services):
        if spans:
            self.send_spans(spans)
        if services:
            now = time()
            if now - self.last_services_flush > self.SERVICES_FLUSH_INTERVAL:
                self.send_services(services)
                self.last_services_flush = now

    def send_spans(self, spans):
        log.debug("Reporting %d spans", len(spans))
        data = encode_spans(spans)
        headers = {}
        self.transport.send("PUT", "/spans", data, headers)

    def send_services(self, services):
        log.debug("Reporting %d services", len(services))
        data = encode_services(services)
        headers = {}
        self.transport.send("PUT", "/services", data, headers)