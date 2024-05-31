import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl


def get_company_data_by_inn(find_inn):
    """ Функция для получения данных об организации по ИНН через публичный API."""
    try:
        # Используем публичный API для получения данных об организации по ИНН
        url = f"https://api.example.com/company/{find_inn}"
        response = requests.get(url)
        response.raise_for_status()  # Проверка на HTTP ошибки
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка при получении данных об организации по ИНН: {e}")
        return None


def extract_email_from_website(url):
    """ Функция для извлечения электронной почты с веб-сайта организации. """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на HTTP ошибки
        soup = BeautifulSoup(response.text, 'html.parser')
        email = None

        # Ищем email в шапке, подвале или разделе контактов
        for tag in soup.find_all(['a', 'p', 'div']):
            if 'mailto:' in tag.get('href', ''):
                email = tag.get('href').replace('mailto:', '')
                break
            elif '@' in tag.text:
                email = tag.text.strip()
                break

        return email
    except requests.RequestException as e:
        print(f"Ошибка при извлечении электронной почты с сайта: {e}")
        return None


def extract_employees_from_website(url):
    """ Функция для извлечения ФИО и должности сотрудников с веб-сайта организации. """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на HTTP ошибки
        soup = BeautifulSoup(response.text, 'html.parser')

        employees = []
        for section in soup.find_all(['section', 'div']):
            if 'Команда' in section.text or 'Руководство' in section.text:
                for person in section.find_all(['p', 'div']):
                    name = person.find('h3') or person.find('b')
                    position = person.find('span') or person.find('i')
                    if name and position:
                        employees.append({
                            'name': name.text.strip(),
                            'position': position.text.strip()
                        })

        return employees
    except requests.RequestException as e:
        print(f"Ошибка при извлечении данных о сотрудниках с сайта: {e}")
        return []


def save_to_excel(data, filename='output.xlsx'):
    """ Функция для сохранения данных в Excel файл. """
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
    except Exception as e:
        print(f"Ошибка при сохранении данных в Excel файл: {e}")


def main(find_inn):
    try:
        company_data = get_company_data_by_inn(find_inn)
        if not company_data:
            print("Не удалось получить данные об организации.")
            return

        website_url = company_data.get('website')
        if not website_url:
            print("Не удалось получить URL сайта организации.")
            return

        email = extract_email_from_website(website_url)
        employees = extract_employees_from_website(website_url)

        data = {
            'company': company_data['name'],
            'email': email,
            'employees': employees
        }

        save_to_excel(data)
        print("Данные успешно сохранены в Excel файл.")
    except Exception as e:
        print(f"Ошибка в основной функции: {e}")


# Пример использования
inn = '1234567890'
main(inn)
