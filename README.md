### Documentation for the Parser

#### Description

This parser accepts the organization's TIN as input and collects the following information from official public sites:

- General email of the organization (office or reception).
- Full names and positions of company employees.

#### Requirements

The following Python libraries are required for the parser to work:

- `requests` for sending HTTP requests.
- `BeautifulSoup` from the `bs4` library for parsing HTML code.
- `pandas` for working with data and saving it to Excel.

Install them using pip:

```sh
pip install requests beautifulsoup4 pandas
```

#### Implementation Steps

1. **Getting Data About an Organization by TIN**

   A public API is used to get data about an organization by TIN.

2. **Extracting Data from Websites**

   - **Extracting Email**

     An organization's email is usually located in the header, footer, or contacts section of a website.

   - **Extracting Employee Names and Positions**

     Employee information is usually located in the "Team", "Management" or "Contacts" section.

3. **Saving Data to Excel**

   The `pandas` library is used to save data to an Excel file.

4. **Main Function**

   Combine all the above steps in the main function.

#### Usage Example

Replace `1234567890` with the required organization's TIN and execute the script. The results will be saved in the `output.xlsx` file.

```python
inn = "1234567890"
main(inn)
```

#### Conclusion

This parser allows you to automatically receive and save in Excel the main contact details and information about employees of an organization by the specified TIN.