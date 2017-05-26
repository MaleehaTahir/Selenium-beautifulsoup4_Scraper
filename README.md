1) Clone the repo

2) Create virtual environment (Use either virtualevn or virtualenvwrapper- depending on preference)

3) pip install -r requirements.txt (Install all the requirements the project needed)

4) A dynamic scraper to extract data from HTML, writing contents to a new csv file and inserting it
   into Azure SQL tables.

5) Ensure that the full directory path to the geckodriver executable has been added to the system path.

5) Ensure that SQL tables have been created in your Azure SQL environment, with the correct number of columns before
   running the scraper.

6) This scraper ran successfully using:
   - FireFox 53.0.2
   - Geckodriver v0.16
   - Selenium 3.4.0

