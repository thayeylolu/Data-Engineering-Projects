
# Data Pipeline for Real-Time Product Data Streaming with Kafka and AWS Service
----

[The Arichture Diagram](Realtime_Kafka_Project.png)
## Introduction

The goal of this project is to create a data pipeline that can handle real-time product data streaming and storage. The data will be streamed using Apache Kafka and processed using various AWS services, including Amazon S3, AWS Glue, and Amazon Athena. The project is intended to provide a blueprint for building real-time data processing systems using Kafka and AWS.


### Process
The following steps are involved in building a data pipeline for real-time product data streaming:

1. Set up an Apache Kafka cluster: 
The first step is to set up a Kafka cluster to receive the data streams. Kafka is a distributed streaming platform that can handle large amounts of data in real-time. It enables the collection, processing, and analysis of real-time data from various sources.

2. Configure a Kafka producer: After setting up the Kafka cluster, the next step is to configure a Kafka producer to send the data streams to the cluster. The producer can be developed in any programming language that has a Kafka client library. For this project, the programming language used was Python. To avoid overloading and breaking the server, a streaming of records where done after 5 seconds. 

Configure a Kafka consumer: The consumer was configured to receive real-time product data streams from the Kafka cluster and process the data in real-time using stream processing.

4. Store the data in Amazon S3: Once the data is streamed to the Kafka cluster, the next step is to store it in Amazon S3.

5. Set up AWS Glue: A Glue crawler is set up to crawl the data in S3 and create a schema in AWS Glue. The crawler created has permssion to access the s3 bucket

5. Query the data using Amazon Athena: . After the data is prepared using AWS Glue, it can be queried using Athena to generate insights.