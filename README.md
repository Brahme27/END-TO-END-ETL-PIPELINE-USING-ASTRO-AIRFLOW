# NASA APOD ETL Pipeline with Apache Airflow, PostgreSQL, and API Integration

## Overview
This project implements an **ETL (Extract, Transform, Load) pipeline** using **Apache Airflow**, **PostgreSQL**, and the **NASA APOD (Astronomy Picture of the Day) API**. The pipeline automates the extraction of daily astronomy images and metadata from NASA's API, transforms the data, and loads it into a PostgreSQL database hosted on **AWS/Astro Cloud**.

## Tech Stack
- **Apache Airflow** (Workflow orchestration)
- **PostgreSQL** (Database for storing APOD data)
- **NASA APOD API** (Data source)
- **AWS/Astro Cloud** (Cloud deployment)

## Pipeline Workflow
1. **Create Table**: Ensures the database table exists before inserting data.
2. **Extract**: Fetches APOD data using NASA's API via an HTTP request.
3. **Transform**: Selects relevant fields and formats the data.
4. **Load**: Inserts transformed data into PostgreSQL.
5. **Verify**: Data can be verified using database queries.

## Deployment Options
This pipeline can be deployed into **Astronomer Cloud**, providing a managed Airflow service for streamlined orchestration. Additionally, the extracted values can be inserted into **AWS RDS (Relational Database Service)** instead of a local PostgreSQL database, allowing for scalable and cloud-based storage solutions.

## Prerequisites
Ensure you have the following installed:
- **Apache Airflow** (with PostgreSQL and HTTP providers)
- **PostgreSQL Database**
- **NASA API Key** (Sign up at [https://api.nasa.gov/](https://api.nasa.gov/))