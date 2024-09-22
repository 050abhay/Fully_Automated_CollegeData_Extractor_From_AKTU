import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Initialize the WebDriver
driver_path = './chromedriver.exe'  # Update the path to your chromedriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Open the website
driver.get("https://kyc.aktu.ac.in/")
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# Step 1: Check if page contains iframe and switch to it
try:
    iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
    driver.switch_to.frame(iframe)
    print("Switched to iframe.")
except Exception:
    print("No iframe found or switching to iframe failed.")

# Step 2: Select "Bachelor of Technology" from the "All Courses" dropdown
try:
    course_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-id="ddlCourses"]')))
    course_dropdown.click()
    print("Dropdown for courses clicked.")
    
    btech_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Bachelor of Technology"]')))
    btech_option.click()
    print("Bachelor of Technology selected.")
    
    time.sleep(3)
    
except Exception as e:
    print(f"Error selecting course: {e}")

# Step 3: Extract college codes and names from the "All Institutes" section
college_data = []

try:
    institute_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-id="ddlInstitute"]')))
    institute_dropdown.click()
    print("Dropdown for institutes clicked.")
    
    institutes = driver.find_elements(By.XPATH, '//ul[@class="dropdown-menu inner"]/li/a/span[@class="text"]')
    
    for institute in institutes:
        text = institute.text
        if text.strip() and "All Institutes" not in text:
            code, name = text.split(maxsplit=1)
            college_data.append((code.strip(), name.strip()))
    
    print(f"Extracted {len(college_data)} institutes.")

except Exception as e:
    print(f"Error extracting institute data: {e}")

# Step 4: Store the extracted college data in a DataFrame
if college_data:
    df_colleges = pd.DataFrame(college_data, columns=['Inst_Code', 'Inst_Name'])
    df_colleges['Inst_Code'] = df_colleges['Inst_Code'].astype(str)  # Ensure Inst_Code is saved as string

    # Save the college data to an Excel file
    df_colleges.to_excel("college_data.xlsx", index=False)
    print("College data saved to college_data.xlsx")
else:
    print("No data to process.")
    driver.quit()
    exit()

# Step 5: Use extracted Inst_Code to fetch course information
data = {}
headers = ['Inst_Code', 'Inst_Name']

for inst_code, inst_name in zip(df_colleges['Inst_Code'], df_colleges['Inst_Name']):
    url = f"https://erp.aktu.ac.in/WebPages/KYC/CollegeDetailedInformation.aspx?Inst={inst_code}%20%20&S=25"
    driver.get(url)
    time.sleep(3)  # Adjust sleep time if needed

    # Find the 'Courses' tab and switch to it
    try:
        driver.find_element(By.XPATH, "//a[@href='#courses']").click()
        time.sleep(2)
        
        # Extract the table data
        table = driver.find_element(By.ID, 'ContentPlaceHolder1_grdCoursesCourse')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # Initialize a dictionary for this institute
        row_data = {'Inst_Code': inst_code.zfill(3), 'Inst_Name': inst_name}

        # Process each row in the table
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, 'td')
            course_name = cols[0].text.strip()
            branch_name = cols[1].text.strip()
            intake_value = int(cols[3].text.strip())

            # Abbreviate the course names
            if 'Master of Computer Applications' in course_name:
                course_name = 'MCA'
            elif 'Masters of Business Administration' in course_name:
                course_name = 'MBA'
            elif 'Bachelor of Technology' in course_name:
                course_name = 'B.Tech'
            elif 'Master of Technology' in course_name:
                course_name = 'M.Tech'

            # Concatenate course name and branch name
            header = f"{course_name} - {branch_name}"

            # Add header if it's not already in headers
            if header not in headers:
                headers.append(header)

            # Fill the intake value under the correct header
            row_data[header] = intake_value

        # Add the row data to the main data dictionary
        data[inst_code] = row_data

    except Exception as e:
        print(f"Error extracting course data for {inst_name}: {e}")

# Step 6: Convert data to DataFrame and save to Excel
df_courses = pd.DataFrame.from_dict(data, orient='index', columns=headers)
output_file = 'institutes_data.xlsx'
df_courses.to_excel(output_file, index=False)
print(f"Course data saved to {output_file}")

# Close the browser
driver.quit()
