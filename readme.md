# Automated Institute and Course Data Scraper for AKTU

## Project Description
The **Automated Institute and Course Data Scraper for AKTU** is a Python-based web scraping project designed to efficiently extract data related to institutes and their courses from the AKTU (Dr. A.P.J. Abdul Kalam Technical University) KYC portal. Utilizing Selenium and Pandas libraries, this project automates the process of navigating the website, selecting the relevant options, and gathering essential information, which is then organized and stored in Excel files for easy access and analysis.

## Features
1. **Web Navigation**: Initializes a Chrome WebDriver and accesses the AKTU KYC portal, maximizing the window for better visibility.
2. **Dynamic Interaction**: Dynamically interacts with dropdown menus to select the "Bachelor of Technology" course and fetch the list of institutes, ensuring a robust user experience.
3. **Data Extraction**: Extracts college codes and names from the "All Institutes" section, handling potential iframe scenarios and utilizing WebDriver waits to ensure elements are fully loaded before interaction.
4. **Structured Data Storage**: Organizes collected data into a Pandas DataFrame, which is then saved as an Excel file, allowing for further analysis or reporting.
5. **Course Information Retrieval**: Retrieves detailed course information, including intake values for each institute, and consolidates it into a comprehensive dataset.


## Benefits
- **Time Efficiency**: Automates tedious data entry tasks, significantly reducing the time required to gather and compile information.
- **Data Accuracy**: Minimizes human error in data collection by using automated methods.
- **Accessibility**: Outputs data in an easily accessible Excel format for stakeholders and analysts.

This project can serve educational institutions, students, and researchers who need to analyze course availability and institute data systematically.

This project not only showcases the utility of web scraping but also provides a practical solution for data management in educational contexts.
