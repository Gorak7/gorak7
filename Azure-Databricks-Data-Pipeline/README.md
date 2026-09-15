# Azure / Databricks Data Pipeline

A portfolio-ready data engineering project demonstrating an Azure cloud workflow with Databricks, PySpark, SQL, and Python.

## Project Overview

This project builds a simple sales analytics pipeline:

**CSV source → Azure Data Lake Storage Gen2 (conceptual) → Databricks / PySpark → Delta Lake → SQL analytics**

The repository includes a local sample dataset so the transformation logic can be tested without requiring an Azure subscription. Azure storage paths can be configured when deploying to a real Azure environment.

## Tech Stack

- Azure Data Lake Storage Gen2
- Azure Databricks
- PySpark
- Python
- SQL
- Delta Lake

## Pipeline Flow

1. **Data ingestion** – Read raw sales CSV data from a local path or Azure Data Lake Storage Gen2.
2. **Transformation** – Clean columns, handle nulls, derive revenue, and standardize dates using PySpark.
3. **Data storage** – Write curated data as Delta Lake tables.
4. **SQL analysis** – Run analytical queries for revenue, product performance, and regional trends.
5. **Azure workflow** – Databricks acts as the processing layer, with ADLS Gen2 as cloud storage. The workflow can be orchestrated with Azure Data Factory in a production deployment.

## Repository Structure

```text
Azure-Databricks-Data-Pipeline/
├── data/
│   └── sales_data.csv
├── src/
│   └── sales_pipeline.py
├── sql/
│   └── analysis.sql
├── requirements.txt
└── README.md
```

## Sample Dataset

The sample data contains order date, region, product, quantity, unit price, and customer segment fields. It is intentionally small for portfolio demonstration and local testing.

## Running in Databricks

1. Upload `data/sales_data.csv` to an ADLS Gen2 container or Databricks volume.
2. Update `INPUT_PATH` in `src/sales_pipeline.py` to the cloud path.
3. Run the PySpark script in an Azure Databricks notebook or job.
4. The curated Delta dataset is written to `OUTPUT_PATH`.
5. Register/query the Delta data and run `sql/analysis.sql`.

### Example Azure paths

```text
abfss://raw@<storage-account>.dfs.core.windows.net/sales/sales_data.csv
abfss://curated@<storage-account>.dfs.core.windows.net/sales/
```

Do not commit Azure access keys, SAS tokens, passwords, or other secrets. Use Azure Databricks secret scopes / managed identity / service principals in a real deployment.

## Key Transformations

- Convert order dates to Spark `date` type
- Cast quantity and unit price to numeric types
- Replace missing customer segments with `Unknown`
- Calculate `revenue = quantity × unit_price`
- Remove invalid records
- Save the curated result in Delta format

## SQL Analysis Examples

The included SQL demonstrates:

- Total revenue
- Revenue by region
- Revenue by product
- Monthly revenue trends
- Top customers by revenue

## Skills Demonstrated

**Azure Cloud | Azure Data Lake Storage Gen2 | Databricks | PySpark | SQL | Python | ETL | Data Cleaning | Delta Lake | Data Analytics**

## Note

This repository contains a reproducible portfolio implementation. Azure resources are represented through configurable cloud paths; no paid Azure infrastructure or credentials are included in the repository.
