import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from typing import Optional, Tuple, List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_company_data_by_inn(find_inn: str) -> Optional[Dict]:
    """Function to get company data by INN through multiple public APIs in Ukraine."""
    sources = [
        f"https://api.youcontrol.com.ua/v1/company/{find_inn}",
        f"https://opendatabot.com/api/v1/company/{find_inn}",
        f"https://api.edr.data.gov.ua/v1/company/{find_inn}",
        f"https://clarity-project.info/api/v1/company/{find_inn}",
        f"https://api.nssmc.gov.ua/v1/company/{find_inn}"
    ]

    for url in sources:
        try:
            logging.info(f"Requesting URL: {url}")
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error getting company data from {url}: {e}")

    logging.error("Failed to get company data from all sources.")
    return None


def extract_info_from_website(url: str) -> Tuple[Optional[str], List[Dict[str, str]]]:
    """Function to extract email and employees' names and positions from the company's website."""
    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()  # Check for HTTP errors
            soup = BeautifulSoup(response.text, "html.parser")

            email = None
            employees = []

            # Search for email in header, footer, or contact section
            for tag in soup.find_all(["a", "p", "div"]):
                if "mailto:" in tag.get("href", ""):
                    email = tag.get("href").replace("mailto:", "")
                    break
                elif "@" in tag.text:
                    email = tag.text.strip()
                    break

            # Search for employees in relevant sections
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

            return email, employees
    except requests.RequestException as e:
        logging.error(f"Error extracting information from website: {e}")
        return None, []


def save_to_excel(data: Dict, filename: str = "output.xlsx") -> None:
    """Function to save data to an Excel file."""
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
    except Exception as e:
        logging.error(f"Error saving data to Excel file: {e}")


def main(find_inn: str) -> None:
    try:
        company_data = get_company_data_by_inn(find_inn)
        if not company_data:
            logging.error("Failed to get company data.")
            return

        website_url = company_data.get("website")
        if not website_url:
            logging.error("Failed to get the company's website URL.")
            return

        email, employees = extract_info_from_website(website_url)

        data = {"company": company_data["name"], "email": email, "employees": employees}

        save_to_excel(data)
        logging.info("Data successfully saved to Excel file.")
    except Exception as e:
        logging.error(f"Error in main function: {e}")


# Example usage
if __name__ == "__main__":
    inn = "1234567890"
    main(inn)