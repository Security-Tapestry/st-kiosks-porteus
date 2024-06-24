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

# Define the date filter for tickets updated since 2022
date_filter = '2022-01-01'

# URL to fetch all tickets updated since 2022-08-01
url = f'https://{FRESH_SERVICE_DOMAIN}.freshservice.com/api/v2/tickets?updated_since={date_filter}'

# Function to fetch all tickets with pagination
def fetch_all_tickets(url, headers):
    tickets = []
    while url:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        if 'tickets' in response_data:
            tickets.extend(response_data['tickets'])
        url = response_data.get('next_page')  # Fetch next page URL
    return tickets

# Fetch all tickets updated since 2022
tickets = fetch_all_tickets(url, headers)

# Initialize counters for ticket statuses by requester_id
requester_ticket_counts = {}

# Count tickets based on their status for each requester
for ticket in tickets:
    status = ticket['status']
    requester_id = ticket.get('requester_id', 'Unknown Requester')
    
    if requester_id not in requester_ticket_counts:
        requester_ticket_counts[requester_id] = {
            'Open': 0,
            'Pending': 0,
            'Resolved': 0,
            'Closed': 0
        }
    
    if status == 2:
        requester_ticket_counts[requester_id]['Open'] += 1
    elif status == 3:
        requester_ticket_counts[requester_id]['Pending'] += 1
    elif status == 4:
        requester_ticket_counts[requester_id]['Resolved'] += 1
    elif status == 5:
        requester_ticket_counts[requester_id]['Closed'] += 1

# HTML template using Jinja2
html_template = """
<!DOCTYPE html>
<html>
<head>
<title>FreshService Ticket Status Report</title>
<style>
        body { font-family: Arial, sans-serif; }
        table { width: 50%; margin: 20px auto; border-collapse: collapse; }
        th, td { padding: 10px; text-align: center; border: 1px solid #ddd; }
        th { background-color: #f4f4f4; }
</style>
</head>
<body>
<h1 style="text-align: center;">FreshService Ticket Status Report</h1>
{% for requester_id, counts in requester_ticket_counts.items() %}
<h2 style="text-align: center;">Requester ID: {{ requester_id }}</h2>
<table>
<tr>
<th>Status</th>
<th>Count</th>
</tr>
<tr>
<td>Open</td>
<td>{{ counts['Open'] }}</td>
</tr>
<tr>
<td>Pending</td>
<td>{{ counts['Pending'] }}</td>
</tr>
<tr>
<td>Resolved</td>
<td>{{ counts['Resolved'] }}</td>
</tr>
<tr>
<td>Closed</td>
<td>{{ counts['Closed'] }}</td>
</tr>
</table>
{% endfor %}
</body>
</html>
"""

# Render the HTML content
template = Template(html_template)
html_content = template.render(requester_ticket_counts=requester_ticket_counts)

# Save the HTML content to a file
with open('docs/kiosk1.html', 'w') as file:
    file.write(html_content)

print("HTML report generated successfully.")
