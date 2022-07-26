# This is a beginner opentelemetry example for Pythonistas


This tutorial code is based on the excellent Medium article [Use Zipkin to Trace Requests in Flask Application](https://medium.com/@eng.mohamed.m.saeed/use-zipkin-to-trace-requests-in-flask-application-68886f02e46) which allows the manual instrumentation of a microservice cluster to zipkin.

The main limitation of that article was py_zipkin. The py_zipkin specific code could not be easily ported to other exporters like [Jaeger](https://www.jaegertracing.io/docs/1.18/opentelemetry/).

Welcome to [Opentelemetry](https://opentelemetry.io/) which is a standrdization effort. This is compliant with many different exporters, comes with plugins sdks and multi language support. 

My aim was mostly pedagogical (I am always a beginner too!!!). So I tried to manually instrument the application with open telemetry with [Openzipkin](https://zipkin.io/) as the original article.

The documentation was not straightforward and not oriented towards beginners. The enlightment came from this [Context Propagation](https://opentelemetry-python.readthedocs.io/en/latest/_modules/opentelemetry/propagate.html). Fortunately the code in comments is in principle correct. Unfortunately it contains some bugs and I had to delve in python code and numerous unfruitful or misleading posts until every piece fell into place.

Naming correctly the services was facilitated by this [Stackoverflow post](https://stackoverflow.com/questions/68819747/add-service-name-in-the-opentelemetry-for-a-javascript-application).

Enjoy!
