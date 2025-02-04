import datetime
from termcolor import colored
import requests
import time

BASE_URL = "https://developers.bolster.ai/api/neo/scan/status"
SCAN_URL = "https://developers.bolster.ai/api/neo/scan"
API_KEY = "ca5u8682x8tk2b32g39lu84guti5qj9usx2pe68i9kn1aic2m70rsrditcv328f4"
HEADERS = {
    'Content-Type': 'application/json',
}

def submit_scan(url):
    """Submit the URL for scanning (quick/full) and return the job ID."""
    payload = {
        "apiKey": API_KEY,
        "urlInfo": {"url": url},
        "scanType": "quick"  # or "full" depending on your choice
    }
    
    response = requests.post(SCAN_URL, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        scan_result = response.json()
        if "jobID" in scan_result:  # Ensure we're checking the correct case (jobID)
            print(f"Scan started. Job ID: {scan_result['jobID']}")
            return scan_result['jobID']
        else:
            print("Error: Job ID not found in the scan response.")
            print(f"Response: {scan_result}")
            return None
    else:
        print(f"Failed to submit scan. HTTP Status code: {response.status_code}")
        return None

def check_scan_status(job_id):
    """Check the status of the scan based on job ID."""
    payload = {
        "apiKey": API_KEY,
        "jobID": job_id,
        "insights": True
    }
    
    response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        scan_result = response.json()
        if "status" in scan_result:  # Ensure we're checking the correct key for status
            return scan_result
        else:
            print("Error: 'status' key is missing in the response.")
            print(f"Response: {scan_result}")
            return None
    else:
        print(f"Failed to retrieve scan status. HTTP Status code: {response.status_code}")
        return None



def display_scan_results(scan_result):
    # Hide Job ID
    print("\nScan Result Summary:")
    print("=" * 50)
    
    # Display URL with color depending on scan result
    phishing_status = scan_result['disposition'].lower()
    url_status_color = 'green' if phishing_status == 'clean' else 'red'
    print(f"URL: {colored(scan_result['url'], url_status_color)}")
    
    # Display phishing status in color
    phishing_status_text = colored(scan_result['disposition'].capitalize(), 'green' if phishing_status == 'clean' else 'red')
    print(f"Discovered Phishing Status: {phishing_status_text}")
    
    # Display brand
    print(f"Brand: {scan_result['brand'] if scan_result['brand'] else 'Unknown'}")
    
    # Display scan status in red (important information)
    print(f"\033[92mScan Status: Done\033[0m" if scan_result['status'] == 'DONE' else f"\033[91mScan Status: {scan_result['status']}\033[0m")

    
    # Display resolved status in red (important)
    resolved_status = 'Resolved' if scan_result['resolved'] else 'Not Resolved'
    #print(f"Resolved: {colored(resolved_status, )}")
    
    # Display scan times
    scan_start_time = datetime.datetime.fromtimestamp(scan_result['scan_start_ts'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    scan_end_time = datetime.datetime.fromtimestamp(scan_result['scan_end_ts'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Scan Start Time: {scan_start_time}")
    print(f"Scan End Time: {scan_end_time}")
    
    # Display screenshot
    print(f"Screenshot Path: {scan_result['screenshot_path']}")
    
    # Display insights link
    print(f"Insights: {scan_result['insights']}")
    
    # Categories detected
    if scan_result['disposition'] == 'scam':
        print("\033[91mCategories Detected:\033[0m")
        for category in scan_result['categories']:
            if isinstance(category, dict):
                # Assuming the category is a dictionary with 'category' and 'score'
                print(f"\033[91m- {category['category']} (Score: {category['score']})\033[0m")
            else:
                # If it's a string (unexpected case), just print the category in red
                print(f"\033[91m- {category}\033[0m")


    else:
        print("No categories detected.")


def scan_phishing_url():

    print(colored("      Welcome to the Phishing Page Scanner Powered by CHECKPHISH Api", "yellow"))
    url_to_scan = input(colored("Enter the URL to scan: ", "green"))
    print("Submitting scan...")
    
    # Submit the scan and get the Job ID
    job_id = submit_scan(url_to_scan)
    
    if job_id:
        print("Checking scan status...")
        
        # Check status and display the results
        scan_results = None
        while not scan_results or scan_results.get('status') != 'DONE':
            scan_results = check_scan_status(job_id)
            if scan_results:
                if scan_results['status'] == 'DONE':
                    display_scan_results(scan_results)
                else:
                    print("Scan in progress... checking status every 5 seconds.")
                    time.sleep(5)
            else:
                break
    else:
        print("Failed to initiate scan.")

if __name__ == "__main__":
    main()

