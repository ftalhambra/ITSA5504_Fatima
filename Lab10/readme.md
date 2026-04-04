# ITSA 5504 – Lab 10
## Testing & Validation of Integrated Systems

This repository contains Lab 10, which demonstrates API contract testing and load testing.

## Tools Used
- Flask (Python)
- Docker
- Pact (Consumer-Driven Contract Testing)
- Apache JMeter

## Description
- A REST API was created using Flask and containerized with Docker.
- Pact was used to execute a consumer test and verify the provider contract.
- Apache JMeter was used to simulate 100 concurrent users over a 5-minute load test.
- Performance metrics such as response time, throughput, and error rate were observed.

## Results
The API handled concurrent load with no errors and stable performance.