![img](docs/assets/airplane-pic.jpeg)

# What

## Real-Time Flight Data Pipeline and ML ETA System

This project demostrates the use of machine learning models within a real-time data processing pipeline. The intended purpose is to accelerate future work of this nature, by establishing software design choices and patterns. 

The end-to-end implementation includes multiple independent components:
1. Data ingestion
    - Aquire data from an API service and push to storage
    - Highly-scalable
    - Supports both historical and real-time ingestion (rather tedious)
2. Data preprocessing
    - Pipiline step to transform and de-deplicate data
    - Make compatible with ML models
3. Data analysis
    - Simply visualize the preprocessed data to gain insight
4. Model training
    - Execute script to create training data
    - Train ML models and log metrics on versioned data
5. Inference
    - Pipeline step to make predictions, using the best ML model.
    - Borrows processing logic from model training repo
6. Model KPIs Live
    - Execute script to measure accuracy of inference predictions.

The primary source of data is the [FlightAware API](https://www.flightaware.com/commercial/aeroapi/) `/flights/ident` endpoint, from which flight status information is retrieved and processed through a series of cloud-based services and tools.

# Why

The goal is to predict estimated arrival times for flights in a manner that is scalable, near-real-time, and supports automatic model re-training on tabular data. The use of Serverless Cloud Functions, Apache Spark, and Delta Lake, significantly simplifies this goal by unifying batch and stream processing.



# Architecture (for now)

![img](docs/assets/GCP-flight-streaming-datalake.jpg)
