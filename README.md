![img](docs/airplane-pic.jpeg)

# Real-Time Flight Data Pipeline and ML ETA System

This repository houses a comprehensive system designed to ingest, preprocess, predict, and visualize estimated arrival times (ETAs) for flights. Utilizing a hybrid architecture, we leverage both streaming and batch processing paradigms to ensure timely and accurate predictions. The primary source of data is the [FlightAware API](https://www.flightaware.com/commercial/aeroapi/) `/flights/ident` endpoint, from which flight status information is retrieved and processed through a series of cloud-based services and tools.

Beyond the core functionalities, this repository serves as a playground to explore alternative methodologies and strategies for predicting flight ETAs and analyzing delays. We encourage experimental modeling techniques, data processing strategies, and any innovative approaches that can enhance the accuracy and efficiency of flight ETA predictions.

# Architecture (for now)

![img](docs/GCP-flight-streaming-datalake.jpg)
