
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
- A cloud function will request flight status data from the FlightAware API and ingest into in a Delta Lake on GCP Cloud Storage, on a frequent basis.
    - Each invocation of the cloud function will collect a single flight identifier. or list of flight identifiers.
    - A one-time job will collect airports of interest and store them in a Delta Table.
    - A daily job will collect flights of interest and store them in a Delta Table.
    - A subsequent daily job will update cloud schedulers for the flights of interest.
    - These cloud schedulers will trigger a Cloud Function to collect the flight data and ingest them into a Delta Table.


1) Initially, a job `query-airports-of-interest.ipynb` will gather and save data on selected airports in a Delta Table `airports-of-interest`.
2) Periodically, another job `query-idents-of-interest.ipynb` gathers a list of flight identifiers associated with the airports of interest and saves them in a Delta Table `idents-of-interest`.

3) A script will deploy cloud schedulers for these selected flights.
    - These schedulers will then activate a Cloud Function `data-ingest-service` to collect and store the flight statuses from the `flights{ident}` endpoint and ingest into a Delta Table.

4) A spark streaming job ingest flight statuses into a delta table, and perform preprocessing and de-duplications

### Data Sources
- flights/{ident}
