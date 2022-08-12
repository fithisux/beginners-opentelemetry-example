import flask
from flask import Flask
import time
import requests
import os
from opentelemetry import propagate, trace, context, baggage
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource, ResourceAttributes
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.zipkin.encoder import Protocol

trace.set_tracer_provider(TracerProvider(resource = Resource({ResourceAttributes.SERVICE_NAME: "foo3-example"})))
tracer = trace.get_tracer(__name__)


app = Flask(__name__)

# create a ZipkinExporter
zipkin_exporter = ZipkinExporter(
    version=Protocol.V1,
    # optional:
    endpoint=os.getenv('ZIPKIN_DSN'),
    # local_node_ipv4="192.168.0.1",
    # local_node_ipv6="2001:db8::c001",
    # local_node_port=31313,
    max_tag_value_length=256,
    # timeout=5 (in seconds),
    # session=requests.Session(),
)

# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(zipkin_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)

PROPAGATOR = propagate.get_global_textmap()

def get_header_from_flask_request(_, request, key):
    return request.headers.get_all(key)

def set_header_into_requests_request(_, request: requests.Request,
                                        key: str, value: str):
    request.headers[key] = value


class SetterGetterHelper:
    set = set_header_into_requests_request
    get = get_header_from_flask_request

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', flask.request.headers)
    app.logger.debug('Body: %s', flask.request.get_data())


def sleep():
    time.sleep(2)
    return 'OK'


@app.route('/')
def index():
    sgh = SetterGetterHelper()
    ctx = PROPAGATOR.extract(
            flask.request,
            None,
            sgh
        )

    app.logger.debug(f"FOO3 ctx {ctx}")

    parentag = baggage.get_baggage('parentag', ctx) or 3
    ctx = baggage.set_baggage('parentag', 3, ctx)
    context.attach(ctx)

    context.attach(ctx)

    with tracer.start_as_current_span("foo3") as current_span:

        current_span.set_attribute("parent.value", parentag)
        sleep()
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
