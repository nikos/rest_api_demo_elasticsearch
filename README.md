# rest_api_demo_elasticsearch  [![Build Status](https://travis-ci.org/nikos/rest_api_demo_elasticsearch.svg?branch=master)](https://travis-ci.org/nikos/rest_api_demo_elasticsearch)  [![Image Info](https://images.microbadger.com/badges/image/nikos/flask-restplus-demo.svg)](https://microbadger.com/images/nikos/flask-restplus-demo)

This repository contains boilerplate code for a RESTful API based on Flask and Flask-RESTPlus in Python.

The code of this demo app is described in an article on my blog:
http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/

It makes use of:
* Python 3
* Flask
* Swagger UI (via `restplus`)
* Simple model (thanks to `elasticsearch-dsl`)
* Alpine Linux (if running as a docker container)


## Getting Started

Either build and run with the help of the provided Dockerfile
```
make build
make run
```
and open up your browser on http://localhost:8000/api/ to see the
Swagger UI and interact with the REST endpoints.

Or run it locally by executing:
```
export PYTHONPATH=.:rest_api_demo
python3 rest_api_demo/app.py
```

See corresponding elasticsearch documents by opening Kibana:

    open http://localhost:5601/