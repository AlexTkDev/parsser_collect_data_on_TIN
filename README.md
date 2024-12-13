# Documentation for the parser

## Description

This parser accepts the organization's TIN as input and collects the following information from official public sites:
- General email of the organization (office or reception).
- Full names and positions of company employees.

## Requirements

### Libraries

The following Python libraries are required for the parser to work:
- `requests` for sending HTTP requests.
- `BeautifulSoup` from the `bs4` library for parsing HTML code.
- `pandas` for working with data and saving it to Excel.

Install them using pip:

```bash
pip install requests beautifulsoup4 pandas
```

## Implementation steps

### 1. Getting data about an organization by TIN

A public API is used to get data about an organization by TIN.

```python
import requests

def get_company_data_by_inn(find_inn):
"""Function for getting company data by TIN via public API."""
try:
# Using public API to get company data by TIN
url = f"https://api.example.com/company/{find_inn}"
response = requests.get(url)
response.raise_for_status() # Check for HTTP errors
return response.json()
except requests.RequestException as e:
print(f"Error getting company data by TIN: {e}")
return None
```

### 2. Extracting data from websites

#### Extracting email

An organization's email is usually located in the header, footer, or contacts section of a website.

```python
from bs4 import BeautifulSoup

def extract_email_from_website(url):
"""A function to extract email from an organization's website."""
try:
response = requests.get(url)
response.raise_for_status() # Check for HTTP errors
soup = BeautifulSoup(response.text, "html.parser")
email = None

# Find email in header, footer, or contacts
for tag in soup.find_all(["a", "p", "div"]):
if "mailto:" in tag.get("href", ""):
email = tag.get("href").replace("mailto:", "")
break
elif "@" in tag.text:
email = tag.text.strip()
break

return email
except requests.RequestException as e:
print(f"Error extracting email from website: {e}")
return None
```

#### Extracting employee names and positions

Employee information is usually located in the "Team", "Management" or "Contacts" section.

```python
def extract_employees_from_website(url):
"""A function to extract employees' names and job titles from an organization's website."""
try:
response = requests.get(url)
response.raise_for_status() # Check for HTTP errors
soup = BeautifulSoup(response.text, "html.parser")

employees = []
for section in soup.find_all(["section", "div"]):
if "Team" in section.text or "Management" in section.text:
for person in section.find_all(["p", "div"]):
name = person.find("h3") or person.find("b")
position = person.find("span") or person.find("i")
if name and position:
employees.append(
{
"name": name.text.strip(),
"position": position.text.strip(),
}
)

return employees
except requests.RequestException as e:
print(f"Error retrieving employee data from the site: {e}")
return []
```

### 3. Saving data to Excel

We use the `pandas` library to save data to an Excel file.

```python
import pandas as pd

def save_to_excel(data, filename="output.xlsx"):
"""Function for saving data to an Excel file."""
try:
df = pd.DataFrame(data)
df.to_excel(filename, index=False)
except Exception as e:
print(f"Error saving data to an Excel file: {e}")
```

### 4. Main function

Combine all the above steps in the main function.

```python
def main(find_inn):
try:
company_data = get_company_data_by_inn(find_inn)
if not company_data:
print("Failed to get company data.")
return

website_url = company_data.get("website")
if not website_url:
print("Failed to get company website URL.")
return

email = extract_email_from_website(website_url)
employees = extract_employees_from_website(website_url)

data = {"company": company_data["name"], "email": email, "employees": employees}

save_to_excel(data)
print("Data successfully saved to Excel file.")
except Exception as e:
print(f"Error in main function: {e}")

# Usage example
inn = "1234567890"
main(inn)
```

## Usage example

Replace `1234567890` with the required organization's TIN and execute the script. The results will be saved in the `output.xlsx` file.

``python
# Usage example
inn = "1234567890"
main(inn)
```

## Conclusion
This parser allows you to automatically receive and save in Excel the main contact details and information about employees of an organization by the specified TIN.
