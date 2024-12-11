
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#define variables

url = "https://akademik.yok.gov.tr/AkademikArama/view/universityListview.jsp"
base_url = "https://akademik.yok.gov.tr"
university_list_url = f"{base_url}/AkademikArama/view/universityListview.jsp"

city = "İSTANBUL"

# check if city is İSTANBUL, go to link if Yes go to next row otherwise

requests.get(url).content
soup = BeautifulSoup(requests.get(url).content,features="lxml")
base_directory = "/Users/gamzeadibelli/OZU DS/CS552/PROJECT/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://akademik.yok.gov.tr",
    "Connection": "keep-alive"
}
    
rows = soup.find_all('tr') 
    
# Check each row for "İSTANBUL"
for row in rows:
    
    columns = row.find_all('td')
    
    data_instructors = []
    data_departments = []
    departments = set()
    
    if columns and city in columns[1].text.strip():

        university_name = columns[0].text.strip() 
        city = columns[1].text.strip()
        link_tag = columns[0].find('a')

        # Create a directory for the university
        output_dir = os.path.join(base_directory, university_name)
        os.makedirs(output_dir, exist_ok=True)
        
        current_url = base_url + link_tag['href']
        current_page=1
        
        
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            })

        # Initial request to get cookies
        response = session.get("https://akademik.yok.gov.tr/AkademikArama/AramaFiltrele?islem=your_initial_url")

        page_number = 1
        
        while True:
            
            # get instructor details - navigate through each page
            uni_response = requests.get(current_url)
            uni_soup = BeautifulSoup(uni_response.content, 'html.parser')
            
            
            with open("result_uni.txt", 'w', encoding='utf-8') as file:
                file.write(uni_soup.prettify())  

            print(uni_soup.prettify())
            
            instructor_rows = uni_soup.find_all('tr', id=lambda x: x and x.startswith('authorInfo_'))

            for row in instructor_rows:

                title = row.find('h6').text.strip()
                name = row.find('h4').text.strip()
            
                details = row.find_all('h6')[1].text.strip()
                details_parts = details.split('/')
                faculty = details_parts[1].strip() if len(details_parts) > 1 else None
                department = details_parts[2].strip() if len(details_parts) > 2 else None

                data_instructors.append({
                    'University': university_name,
                    'Faculty': faculty,
                    'Department': department,
                    'Title': title,
                    'Name': name
                    })
                
                if department not in departments:
                    departments.add(department)
                    data_departments.append({
                        'University': university_name,
                        'Department': department
                        })

            # check if pagination exists
            # check if next page number exists, if yes go to its link
            # if no, check >> button, go to its link
            
            page_number += 1
            
            pagination = uni_soup.find('ul', class_='pagination')
        
            # Check for the next page number
            next_page_url = None
            page_found = False
            page_links = pagination.find_all('a')
        
            for link in page_links:
                if link.text.strip() == str(page_number):  # Look for the next page number
                    next_page_url = base_url + link['href']
                    page_found = True
                    break
        
            if page_found:
               
                current_url = next_page_url
                print(current_url)
            else:
                print(f"Page {page_number} not found")
                break

        df = pd.DataFrame(data_instructors)
        output_file = os.path.join(output_dir, f"{university_name}.xlsx")
        df.to_excel(output_file, index=False)

        
        # Write departments to excel
        df2 = pd.DataFrame(data_departments)
        output_file = os.path.join(output_dir, f"{university_name}_departments.xlsx")
        df2.to_excel(output_file, index=False)


