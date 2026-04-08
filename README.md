# modern-lakehouse

## Idea
The idea of this repository is to build a modern datalakehouse using several components based on DuckLake. 
For that purpose full pipeline might be a Kafka-topic as starting point, and then a Kafka-connect instance within a 
s3 compatible Sink into a Minio Instance and then on top of that the DuckLake and a PostgreSQL for the ducklake catalog


