import os
import requests
from jinja2 import Template

FRESH_SERVICE_DOMAIN = 'securitytapestry'

def getAPIKey():
    API_KEY = os.getenv("FRESH_SERVICE_API_KEY")
    if str(API_KEY) == "":
        print("NO FS API KEY FOUND")
    return API_KEY

# Define the headers for authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {getAPIKey()}'
}
 
# URL to fetch all tickets
url = f'https://{FRESH_SERVICE_DOMAIN}.freshservice.com/api/v2/tickets'
 
# Fetch tickets
response = requests.get(url, headers=headers)

tickets = response.json()['tickets']
 
# Initialize counters for ticket statuses
status_counts = {
    'Open': 0,
    'Pending': 0,
    'Resolved': 0,
    'Closed': 0
}
 
# Count tickets based on their status
for ticket in tickets:
    status = ticket['status']
    if status == 2:
        status_counts['Open'] += 1
    elif status == 3:
        status_counts['Pending'] += 1
    elif status == 4:
        status_counts['Resolved'] += 1
    elif status == 5:
        status_counts['Closed'] += 1
 
# HTML template using Jinja2
html_template = """
<!DOCTYPE html>
<html>
<head>
<title>FreshService Ticket Status Report</title>
<style>
        body { font-family: Arial, sans-serif; }
        table { width: 50%; margin: 0 auto; border-collapse: collapse; }
        th, td { padding: 10px; text-align: center; border: 1px solid #ddd; }
        th { background-color: #f4f4f4; }
</style>
</head>
<body>
<h1 style="text-align: center;">FreshService Ticket Status Report</h1>
<table>
<tr>
<th>Status</th>
<th>Count</th>
</tr>
<tr>
<td>Open</td>
<td>{{ open }}</td>
</tr>
<tr>
<td>Pending</td>
<td>{{ pending }}</td>
</tr>
<tr>
<td>Resolved</td>
<td>{{ resolved }}</td>
</tr>
<tr>
<td>Closed</td>
<td>{{ closed }}</td>
</tr>
</table>
</body>
</html>
"""
 
# Render the HTML content
template = Template(html_template)
html_content = template.render(
    open=status_counts['Open'],
    pending=status_counts['Pending'],
    resolved=status_counts['Resolved'],
    closed=status_counts['Closed']
)
 
# Save the HTML content to a file
with open('docs/index.html', 'w') as file:
    file.write(html_content)
 
print("HTML report generated successfully.")