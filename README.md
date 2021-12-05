# TrackingMicroservices
John Deere ISG-K Digital Application, Backend Code Challenge

## Architecture
This implementation lies on the *MVC* concept, where the API just catches the request and pass the *body* object to the **Controller**. The *controller*, then, may apply some *validation* on the input and finally, call the required **db** function from the **DataLayer**. 

Meanwhile, the concept of **View Model** is implemented as well, in order to have a concrete structure for the data.

## TMS_API.py
The Api locates in the module *tms_api.py*, so for running the api, just run this module.

## Event_Producer.py
This module, just contains an *Interface* for hadning over the request to the **consumer** microservice. This Interface has not been implemented, but we assume that the functionality will be provided eventually.

## Event_Consumer.py
This module is an *Interface* as well. It is assumed that it works fine, but no implementation for this available now.

## config.ini
There are some configuration, in which one can change them easeily via **config.ini**.
It contains different sections as follow:
1. **GENERAL**
2. **LOGS**
Contains the neccessary configs for the logging object, such as the *name, file path, and the logging level*
3. **DB**
Contains the **environment variables** which hold the db credential.
* Note: Before runing the API, make sure that you already have these *environment variables* with the correct values.
4. **TMS_API**
Contains some configs regarding running the API, such as *debug_mode*.
5. **VALIDATIONS**
Contains some constant variables for validation purpose, such as max_event_count.


