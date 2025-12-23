import requests
import json

# Test data - simple sequential S-box
test_sbox = list(range(256))

# Test the download endpoint
print("Testing download Excel endpoint...")
response = requests.post('http://127.0.0.1:5000/api/sbox/download-excel', 
                        json={'sbox': test_sbox})
if response.status_code == 200:
    with open('downloaded_sbox.xlsx', 'wb') as f:
        f.write(response.content)
    print("Download Excel test: PASSED - File downloaded successfully")
else:
    print(f"Download Excel test: FAILED - Status code {response.status_code}, Response: {response.text}")

# Test the upload endpoint
print("\nTesting upload Excel endpoint...")
files = {'file': open('test_sbox.xlsx', 'rb')}
response = requests.post('http://127.0.0.1:5000/api/sbox/upload-excel', files=files)
files['file'].close()

if response.status_code == 200:
    result = response.json()
    if result['ok'] and result['sbox'] == test_sbox:
        print("Upload Excel test: PASSED - S-box data matches expected values")
    else:
        print(f"Upload Excel test: FAILED - Data mismatch. Expected: first few values {test_sbox[:5]}, Got: {result['sbox'][:5]}")
        print(f"Full response: {result}")
else:
    print(f"Upload Excel test: FAILED - Status code {response.status_code}, Response: {response.text}")

print("\nTesting completed.")