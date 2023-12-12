![img](docs/assets/airplane-pic.jpeg)

# Real-Time Flight Data Pipeline and ML ETA System

This repository houses a set of components to ingest, preprocess, visualiize, and predict estimated arrival times (ETAs) for flights in a manner that supports a balance of scalability, low latency processing, and ease of use. By leveraging Cloud Functions, Apache Spark, and Delta Lake, we can leverage both streaming and batch processing paradigms to ensure timely predictions and consistent processing logic. 

The primary source of data is the [FlightAware API](https://www.flightaware.com/commercial/aeroapi/) `/flights/ident` endpoint, from which flight status information is retrieved and processed through a series of cloud-based services and tools.

# Architecture (for now)

![img](docs/assets/GCP-flight-streaming-datalake.jpg)
