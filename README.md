# A Shared Gas Mileage diary
#### A Distributed systems course project for the University of Oulu
Group members:
- Tarek Ali, tali22@student.oulu.fi
- Petri Jaakkola, pjaakkol18@student.oulu.fi
- Sadeep Batewela Vidanelage, Sadeep.Batewela.Vidanelage@student.oulu.fi
- Oskar Byman, oskar.byman@student.oulu.fi


## Summary
This project consists of an mileage diary for sharing car usage data. Currently the implementation is only a Proof-Of-Concept where no additional business logic is implemented.

## Architecture
The architecture consists of three distributed parts, a zookeeper instance for maintaining the kafka cluster, a kafka-service which handles the topics and events and a client application that is used to send and receive data from the kafka-service.

## How to run:
### Dependencies:
1. Docker
1. Python3

### Steps to launch
1. Install python requirements: `python -m pip install -r requirements.txt`
1. Run the Zookeeper and Kafka services with Docker compose: `docker compose up`
1. Launch the client application: `python client/SharedGasMileageDiary.py`

### Usage:
- Enter Driver name.
- Enter the start kilometers from the car odometer before starting driving.
- Enter the end kilometer from the car odometer after the drive.
- If car was fueled enter fuel amount in euros.

## Improvements/Missing features
- Application logic for calculating the cost per driver

