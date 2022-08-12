import flask
from flask import Flask
import os
import requests
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource, ResourceAttributes
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.zipkin.encoder import Protocol

trace.set_tracer_provider(TracerProvider(resource = Resource({ResourceAttributes.SERVICE_NAME: "foo2-example"})))
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

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', flask.request.headers)
    app.logger.debug('Body: %s', flask.request.get_data())


def call_api_03():
    requests.get('http://api_03:5000/')
    return 'OK'


@app.route('/')
def index():

    app.logger.debug(f"FOO2 rq {flask.request.headers}")

    with tracer.start_as_current_span("foo2"):

        call_api_03 = requests.Request(
            "GET", "http://api_03:5000/"
        )

        app.logger.debug(f"FOO2 {call_api_03.headers}")

        session = requests.Session()
        session.send(call_api_03.prepare())
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)

