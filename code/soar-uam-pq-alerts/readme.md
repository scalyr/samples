# **SentinelOne Alert Handling Script**

## **Overview**

This script is designed to facilitate the ingestion and processing of alerts from SentinelOne's Power Query API. It loads alert data, updates it with additional information retrieved from SentinelOne, and then sends the alert to S1 Unified Alerts Management console.

## **Features**

* **Alert Ingestion**: The script fetches alert data from a local file.  
* **Data Enrichment**: It queries SentinelOne for additional data, such as process names and MD5 hashes, based on specific queries.  
* **Alert Processing**: Updates the alert data with the enriched information (e.g., process name and MD5 hash).  
* **Alert Egress**: Sends the updated alerts to an external ingestion endpoint via an HTTP POST request.

## **Requirements**

* Python 3.x  
* `requests` library  
* `gzip` and `json` modules (standard Python libraries)  
* SentinelOne API token  
* SentinelOne account ID  
* Site ID (optional)

## **Environment Variables**

The following environment variables must be set for the script to function properly:

* `SENTINELONE_TOKEN`: Your SentinelOne API token.  
* `ACCOUNT_ID`: Your SentinelOne account ID.  
* `SITE_ID` (optional): Your SentinelOne site ID (if applicable).

## **Setup**

1.  Install the required Python packages:  
`pip install requests`

2.  Set the required environment variables:  
   * `SENTINELONE_TOKEN`  
   * `ACCOUNT_ID`  
   * `SITE_ID` (optional)  
3.  Place the alert JSON file that contains the basic alert data (e.g., `alert.json`), which will be updated by the script.
4.  execute `python3 run.py`

