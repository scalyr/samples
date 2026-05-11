import os
import requests
import gzip
import json
import uuid
import time
import logging


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def egress_uam_alert(alert, scope, token, uam_ingest_url):
    headers = {
        "Authorization": f"Bearer {token}",
        "S1-Scope": scope,
        "Content-Encoding": "gzip",
        "Content-Type": "application/json"
    }

    # Convert the alert to JSON and gzip it
    gzipped_alert = gzip.compress(json.dumps(alert).encode('utf-8'))
    logger.info("Compressed alert data and prepared headers for request.")

    try:
        logger.info("Sending POST request to SentinelOne endpoint.")
        response = requests.post(f"{uam_ingest_url}/v1/alerts", headers=headers, data=gzipped_alert)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        logger.info("Request successful with status code: %s", response.status_code)
        return {
            "status": response.status_code,
            "statusText": response.reason,
            "data": response.json(),
        }
    except requests.exceptions.RequestException as err:
        logger.error("Request error: %s", err)
        return None

def load_alert_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            alert = json.load(file)
        logger.info("Loaded alert from file: %s", file_path)
    except Exception as e:
        logger.error("Error loading alert file: %s", e)
        return None
    
    timeDst = int(time.time() * 1000)  # Generate current timestamp in milliseconds
    logger.info("Generated timestamp: %s", timeDst)

    # Replace UID and time with generated values
    alert["finding_info"]["uid"] = str(uuid.uuid4())  # Auto-generate unique identifier (UID)
    alert["time"] = timeDst  # Auto-generate current timestamp in milliseconds
    logger.info("Assigned UID and timestamp to alert.")

    return alert

def query_sentinelone(query, start_time, end_time, token, scope):
    url = "https://xdr.us1.sentinelone.net/api/powerQuery"
    payload = json.dumps({
        "query": query,
        "startTime": start_time,
        "endTime": end_time
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'S1-Scope': scope  # Confirm account_id here if it's the correct scope identifier
    }

    try:
        logger.info("Sending query to SentinelOne powerQuery API.")
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Ensure we notice bad responses
        logger.info("Query successful with status code: %s", response.status_code)
        
        try:
            # Try to parse JSON response
            response_json = response.json()
            logger.debug("Parsed response: %s", response_json)
            
            # Check if the 'values' field exists and contains data
            if not response_json or 'values' not in response_json or not response_json['values']:
                logger.warning("No valid data found in response. Could not update alert.")
                return None

            # Return the data (values) from the response
            return response_json
        
        except ValueError as e:
            logger.error("Error parsing JSON response: %s", e)
            return None

    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s - Response content: %s", http_err, response.text)
    except Exception as err:
        logger.error("Other error: %s", err)
    
    return None

def update_alert_with_process_name_and_md5(alert, query_result, row_index):
    try:
        logger.debug("Query result: %s", query_result)  # Log the entire response for inspection
        
        if "columns" in query_result and "values" in query_result:
            logger.debug("Columns: %s", query_result["columns"])
            logger.debug("Values: %s", query_result["values"])

            # Extract column names and their indices
            column_names = [col["name"] for col in query_result["columns"]]
            logger.debug("Column names: %s", column_names)
            
            # Extract the process name and MD5 hash columns independently
            process_name_index = None
            md5_index = None
            
            if "src.process.file.name" in column_names:
                process_name_index = column_names.index("src.process.file.name")
                logger.debug("Process name index: %d", process_name_index)
            
            if "md5" in column_names:
                md5_index = column_names.index("md5")
                logger.debug("MD5 hash index: %d", md5_index)

            # Get the specific row based on the index
            row = query_result["values"][row_index]
            
            # Process name update
            if process_name_index is not None:
                process_name = row[process_name_index]
                logger.debug("Extracted process name: %s", process_name)
                
                # Update the alert's "evidences.process.file.name" with this value
                if "evidences" in alert and alert["evidences"]:
                    alert["evidences"][0]["process"]["file"]["name"] = process_name
                    logger.info("Updated evidences.process.file.name with value: %s", process_name)
                else:
                    logger.warning("No evidences found in the alert to update process name.")

            # MD5 hash update
            if md5_index is not None:
                md5_value = row[md5_index]
                logger.debug("Extracted MD5 hash: %s", md5_value)

                # Check if "evidences.process.file.hashes" exists in the alert
                if "evidences" in alert and alert["evidences"] and "process" in alert["evidences"][0]:
                    file_data = alert["evidences"][0]["process"]["file"]
                    if "hashes" in file_data:
                        # Search for an existing MD5 hash with algorithm_id 1
                        md5_hash_found = False
                        for hash_entry in file_data["hashes"]:
                            if hash_entry.get("algorithm_id") == 1:  # MD5 has algorithm_id 1
                                hash_entry["value"] = md5_value  # Update the MD5 hash value
                                md5_hash_found = True
                                logger.info("Updated MD5 hash (algorithm_id 1) with value: %s", md5_value)
                                break

                        # If no existing MD5 hash was found, add a new entry
                        if not md5_hash_found:
                            file_data["hashes"].append({"algorithm_id": 1, "value": md5_value})
                            logger.info("Added new MD5 hash (algorithm_id 1) with value: %s", md5_value)
                    else:
                        # If "hashes" is missing, initialize it
                        file_data["hashes"] = [{"algorithm_id": 1, "value": md5_value}]
                        logger.info("Initialized MD5 hashes with value: %s", md5_value)
                else:
                    logger.warning("No hashes found in the alert to update.")
        else:
            logger.warning("Unexpected query result format. Could not update alert.")
            
    except (IndexError, KeyError) as e:
        logger.error("Error extracting process name or MD5 hash: %s", e)





# Example usage
if __name__ == "__main__":
    token = os.getenv("SENTINELONE_TOKEN")
    account_id = os.getenv("ACCOUNT_ID")
    site_id = ""  # Default to empty if SITE_ID is not set
    logger.info("Environment variables loaded. Token: %s, Account ID: %s, Site ID: %s", token, account_id, site_id)

    if not token or not account_id:
        logger.error("Missing necessary environment variables.")
        exit(1)

    # Define scope and prepare for egress
    scope = f"{account_id}"
    logger.info("Scope: %s", scope)

    # Load alert data from JSON file
    alert_file_path = "alert.json"
    

    # Query SentinelOne for additional data
    query = "|union (|limit 1 | columns src.process.file.name= 'hello', md5 = '5eb63bbbe01eeed093cb22bb8f5acdc3'), (|limit 1 | columns src.process.file.name= 'world', md5 = '7d793037a0760186574b0282f2f435e7')"  # Define your actual query
    start_time = "1h"  # Last 7 days in milliseconds
    end_time = "0h"
    query_result = query_sentinelone(query, start_time, end_time, token, scope)

    # Loop through each row in the query result and send a separate alert for each
    if query_result:
        for i, row in enumerate(query_result['values']):
            alert = load_alert_from_file(alert_file_path)
            if alert is None:
                logger.error("Failed to load alert data. Exiting.")
                exit(1)
            
            logger.info("Processing row %d: %s", i, row)
            
            # Pass the row and its index to the update function
            update_alert_with_process_name_and_md5(alert, query_result, i)  # Pass the index and full query result
            
            # Define UAM ingest URL
            uam_ingest_url = "https://ingest.us1.sentinelone.net"
            response = egress_uam_alert(alert, scope, token, uam_ingest_url)
            
            if response:
                logger.info("Egress successful for row %d. Response: %s", i, response)
            else:
                logger.error("Egress failed for row %d.", i)
    else:
        logger.error("Query failed or returned no data. Proceeding without update.")
