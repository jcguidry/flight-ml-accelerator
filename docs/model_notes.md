As far as Estimated Time of Arrival (ETA) is concerned, there are multiple modeling techniques and paradigmns that can be used to predict the ETA of a given trip.

The possible approaches are conditioned by following factors:
    - Desired time of use: Is the trip in the future, or is it in progress? (i.e. when the ETA is requested)
    - Available data: What is the data like? How are events represented?
    - Desired granularity: Should the trip be broken into segments? (i.e. is there a scheduled sequence of events?)
    - Desired Output: Single ETA, sequence of ETAs, distribution, probability, or time window?

There are the main approaches to modeling ETA:
    - **Schedule-based**: The ETA is modeled as a **function of a sequence of events/segments (a schedule)**.
        Usage:
            - Ideal for predicting the ETA of a trip in the future.
            - Can be used to predict the ETA of a trip in progress, but only if the trip is broken into segments.
        - Methodology:
            - The model predicts the duration of each event/segment individually.
                - Each event duration can be simply aggregated to calculate ETA.
                - Alternatively, each event duration can be used to calculate the start time of the next event.
    - **Current-state-based**: The ETA is modeled as a **function of the current state of a trip**.
        - Usage:
            - Ideal for predicting the real-time ETA of a trip in progress.
            - Suited for big data scenarios when desired output is classification or time window.
        - Metholodogy:
            - The model predicts the duration from the current event to the end of the trip, as a single-shot.
                - The model can update the ETA as new data becomes available.
            - Data must be available in the form of events. e.g. arrivals and departures
    - **Sequential-ongoing-state-based**: The ETA is modeled as a **function of the current state of the trip and the history of the trip.**
        - Usage:
            - Ideal for predicting the ETA of a trip in future or in progress, with greater accuracy than a current-state-based model.
        - Methodology
            - The model predicts the duration of each event/segment in a sequential manner, predicting the next event/segment based on previous ones observed or predicted.
                - The model can update the ETA as new data becomes available or with only the schedule available.
            - Use a sequential model (RNN, LSTM, etc.) to model the ETA as a function of the current state of the trip and the history of the trip.
            - Ongoing trip provides information about the current state of the trip that is not available in the current state of the trip.
    - *Residual duration modeling*: The ETA is modeled as a the difference between an existing ETA and actual arrival time.
        - If an existing "naive" scheduled or estimated time is available, the model can predict a residual offset from that time.
            - Usage:
                - If the existing time is a decent estimate, but the model can improve it.
                - If low latency is desired, and modeling of the entire trip is complex or too slow.


Below is a table that summarizes the approaches and their usage:

| Approach                        | Usage                                                                                                                                                     | Methodology                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Schedule-based                  | Ideal for predicting the ETA of a trip in the future. Can be used to predict the ETA of a trip in progress, but only if the trip is broken into segments. | The model predicts the duration of each event/segment individually. Each event duration can be simply aggregated to calculate ETA. Alternatively, each event duration can be used to calculate the start time of the next event.                                                                                                                                                                                                                                                                                                  |
| Current-state-based             | Ideal for predicting the real-time ETA of a trip in progress. Suited for big data scenarios when desired output is classification or time window.         | The model predicts the duration from the current event to the end of the trip, as a single-shot. The model can update the ETA as new data becomes available. Data must be available in the form of events. e.g. arrivals and departures                                                                                                                                                                                                                                                                                           |
| Sequential-ongoing-state-based  | Ideal for predicting the ETA of a trip in future or in progress, with greater accuracy than a current-state-based model.                                  | The model predicts the duration of each event/segment in a sequential manner, predicting the next event/segment based on previous ones observed or predicted. The model can update the ETA as new data becomes available or with only the schedule available. Use a sequential model (RNN, LSTM, etc.) to model the ETA as a function of the current state of the trip and the history of the trip. Ongoing trip provides information about the current state of the trip that is not available in the current state of the trip. |
| Modeling of a residual duration | If an existing "naive" scheduled or estimated time is available, the model can predict a residual offset from that time.                                  | If the existing time is a decent estimate, but the model can improve it. If low latency is desired, and modeling of the entire trip is complex or too slow.                                                                                                                                                                                                                                                                                                                                                                       |
