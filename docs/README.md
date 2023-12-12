
# Flight ML ETA Prediction Roadmap

- Data Engineering and Machine Learning project to predict flight delays and arrival times.


## Problem Definition and Scope
- The goal of this project is to predict the arrival time of a flight based on the data available at the time of departure. The project will be developed in Python and will use the following technologies:
- Google Cloud Platform
- GCP Cloud Functions
- Delta Lake
- Apache Spark
- Python Pandas/Polars
- Python Scikit-Learn / AutoML / PyTorch

## Data Collection and Management
1)  Cloud functions used to request flight status data from the FlightAware API and ingest into in a Delta Lake Table on GCS.
    - The functions are triggered by Cloud Schedulers, which send JSON messages containing flight IDs to be ingested.
    - A one-time job collects airports of interest to configure/update the cloud schedulers.
    

    1.4) A spark streaming job ingest flight statuses into a delta table, and perform preprocessing and de-duplications

### Data Sources
- flights/{ident}





### Outstanding Tasks

- [ ] asd
