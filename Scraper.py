# -*- coding: utf-8 -*-
import csv
import pyodbc
import time

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        NoAlertPresentException,)
from bs4 import BeautifulSoup


class RunScraper:
    """ Web page data scraper

    This scrapes data from webpages,
    writes the contents to a new csv each time it's executed
    and inserts the data into an Azure SQL database.
    """

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "homepage_url"
        self.verificationErrors = []
        self.accept_next_alert = True

    def scraper(self):
        print("Running scraper")
        driver = self.driver
        driver.get("target_page_url")
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("enter_username")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("enter_Password")
        driver.find_element_by_css_selector("path to css_selector").click()
        time.sleep(5)
        driver.find_element_by_xpath("path to element_id in xpath").click()
        driver.find_element_by_id("element_id").click()
        time.sleep(5)

        nine_columnns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        twelve_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        headers, data = scrape_page(driver.page_source, nine_columnns)

        csv_file = write_csv('csv_file_name', headers, data)
        csv_to_db(csv_file, 'db_tbl_name')

        driver.find_element_by_id("element_id").click()
        driver.find_element_by_id("element_id").click()
        time.sleep(5)

        headers, data = scrape_page(driver.page_source, nine_columnns)
        csv_file = write_csv('csv_file_name', headers, data)
        csv_to_db(csv_file, 'db_tbl_name')

        driver.find_element_by_id("element_id").click()
        driver.find_element_by_id("element_id").click()
        time.sleep(5)

        headers, data = scrape_page(driver.page_source, nine_columnns)
        csv_file = write_csv('csv_file_name', headers, data)
        csv_to_db(csv_file, 'db_tbl_name')

        driver.find_element_by_xpath("path to element_id in xpath").click()
        time.sleep(5)
        driver.find_element_by_id("element_id").click()
        time.sleep(5)

        headers, data = scrape_page(driver.page_source, twelve_columns)
        csv_file = write_csv('csv_file_name', headers, data)
        csv_to_db(csv_file, 'db_tbl_name')

        driver.find_element_by_id("element_id").click()
        driver.find_element_by_id("element_id").click()
        time.sleep(5)

        headers, data = scrape_page(driver.page_source, twelve_columns)
        csv_file = write_csv('csv_file_name', headers, data)
        csv_to_db(csv_file, 'db_tbl_name')

        driver.find_element_by_id("element_id").click()
        driver.find_element_by_id("element_id").click()

        headers, data = scrape_page(driver.page_source, twelve_columns)
        csv_file = write_csv('csv_file_name', headers, data)
        csv_to_db(csv_file, 'db_tbl_name')

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.close()
        self.assertEqual([], self.verificationErrors)


def scrape_page(page_source, columns):
    """scrapes headers & data from HTML page"""

    soup = BeautifulSoup(page_source, 'html.parser')

    print(soup)
    table = soup.find('table', {'id': "table_id"})
    print(table)

    headers = []
    header_elements = table.find_all('th')

    for header in header_elements:
        headers.append(header.get_text().strip())
    data = []

    for row in table.find_all('tr'):
        elements = row.find_all('td')
        row_data = []
        for i in range(len(elements)):
            if i in columns:
                row_data.append(elements[i].get_text().strip())
        data.append(row_data)
    return headers, data


def write_csv(filename, headers, data):
    """This writes to csv file given to it."""

    current_timestamp = time.localtime()
    current_date = time.strftime("%d/%m/%Y", current_timestamp)
    current_time = time.strftime("%H:%M:%S", current_timestamp)
    filename = '{}-{}-{}.csv'.format(
        filename, current_date.replace('/', ''), current_time.replace(':', '')
    )

    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers + ['Current_Date'] + ['Current_Time'])
        for row in data:
            if any(field.strip() for field in row):
                row.extend([current_date, current_time])
                csv_writer.writerow(row)
    return filename


# connect to sql server
conn = pyodbc.connect(
    server='server_name',
    port='',
    user='Username',
    password='Password',
    driver='{SQL Server}',
    database='database_name'
)

cursor = conn.cursor


def csv_to_db(filename, table_name):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(header)

        placeholders = ['?'] * len(header)
        query = 'INSERT INTO {} VALUES({})'.format(
            table_name, ', '.join(placeholders)
        )

        for csv_rows in reader:
            conn.execute(query, csv_rows)
            conn.commit()


if __name__ == '__main__':
    t = RunScraper()
    t.scraper()
