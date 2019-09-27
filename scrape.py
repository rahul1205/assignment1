import mysql.connector

import requests
from bs4 import BeautifulSoup

#db handler
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="assignment1b"
) 

page_links = []

def get_soup(url):
    """
    Utility function to make an HTTP request and return BeautifulSoup instance
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    return soup


def find_faculties_and_departments():
    """
    Scrapes Faculty Page and returns faculties and their respective departments
    """
    url = "https://www.dal.ca/academics/faculties.html"
    soup = get_soup(url)

    faculties = soup.find_all('div', attrs={'class':'text parbase section'})


    faculties_dict = {}
    # print (a)
    for f in faculties[1:]:
        faculty_name = (f.find('h2').text.strip())
        departments = []
        if f.find_next_sibling()['class'][0] == 'expandingSubsection':
            department_list = f.find_next_sibling().find_all('li')
            for d in department_list:
                departments.append(d.text.strip().replace('\xa0&', ''))
        faculties_dict[faculty_name] = departments

    return faculties_dict



def build_xml_faculty():
    """
    Utility function to create XML string for Faculty table
    """
    faculty_and_department = find_faculties_and_departments()
    faculties = faculty_and_department.keys()
    xml_faculty = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"faculty\">"
    for i, f in enumerate(faculties):
        xml_faculty = xml_faculty + "<row>" + \
                        "<field name=\"faculty_id\">" + str(i) + \
                        "</field><field name=\"faculty_name\">" + f.strip() + \
                        "</field><field name=\"Campus_campus_id\">" + '1' + \
                        "</field></row>"
    xml_faculty = xml_faculty + "</table_data></database>"

    return xml_faculty



def build_xml_department():
    """
    Utility function to create XML string for Department with foreign key faculty (* Departments Scrapped, 56 Records in XML; average runtime =30 seconds)
    """
    cursor = mydb.cursor()
    cursor.execute("SELECT faculty_name, faculty_id FROM faculty")
    faculty_db_dict = dict(cursor.fetchall()) # fetches all records from populated faculty table and returns a dictionary as {faculty_name:faculty_id} 

    faculty_and_department = find_faculties_and_departments() # calls the scraping function

    faculties = faculty_and_department.keys()
    xml_department = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"department\">"

    counter = 0  #maintains primary key for department
    for f in faculties: # iterates through all faculties scrapped
        departments = faculty_and_department.get(f)
        current_faculty_id = faculty_db_dict.get(f)
        
        for d in departments: # iterates through departments of faculty in current iteration
            counter = counter+1
            xml_department = xml_department + "<row>" + \
                                "<field name=\"department_id\">" + str(counter) + \
                                "</field><field name=\"department_name\">" + d.strip().replace('&', 'and') + \
                                "</field><field name=\"Faculty_faculty_id\">" + str(current_faculty_id) + \
                                "</field></row>"
    xml_department = xml_department + "</table_data></database>"

    return xml_department


def scrape_and_build_program_xml():
    """
    Utility function to fetch programs and build a XML string
    """

    cursor = mydb.cursor()
    cursor.execute("SELECT department_name, department_id FROM department")
    departments_db_dict = dict(cursor.fetchall())

    # department_names_list = departments_db_dict.keys()

    url = "https://www.dal.ca/academics/faculties.html"
    soup = get_soup(url)

    departments = soup.find_all('li') # fetches all departments

    # print (a)
    xml_program = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"program\">"
    count = 0

    for dep in departments:
        current_dep_id = departments_db_dict.get(dep.text.strip().replace('\xa0&', '').replace('&', 'and'))
        

        if current_dep_id and current_dep_id<5: # FACULTY OF AGRICULTURE
            
            department_page_link = dep.find('a')['href'] # gets link of the department home page
            if not 'http:' in department_page_link:
                department_page_link = "http://www.dal.ca" + department_page_link

            soup = get_soup(department_page_link)
            program_div = soup.find('div', attrs={'class':'sb-highlight-box-content clearfix'})


            if current_dep_id == 1: # corner case for AGRICULTURE department 1 (missing a heading, so need to code it seperately)
                degree_type = 'undergraduate'
                programs = program_div.find('ul').find_all('li') # gets first UL

                for prog in programs:
                    count = count + 1
                    xml_program = xml_program + "<row>" + \
                                "<field name=\"program_id\">" + str(count) + \
                                "</field><field name=\"program_name\">" + prog.text.strip().replace('&', 'and') + \
                                "</field><field name=\"program_type\">" + degree_type + \
                                "</field><field name=\"Department_department_id\">" + str(current_dep_id) + \
                                "</field></row>"

                degree_types = program_div.find_all('h4') # finds more type of courses
                for deg in degree_types:
                    degree_type = deg.text.strip().lower()
                    programs= deg.find_next('ul').find_all('li')

                    for prog in programs:
                        count = count + 1
                        xml_program = xml_program + "<row>" + \
                                    "<field name=\"program_id\">" + str(count) + \
                                    "</field><field name=\"program_name\">" + prog.text.strip().replace('&', 'and') + \
                                    "</field><field name=\"program_type\">" + degree_type + \
                                    "</field><field name=\"Department_department_id\">" + str(current_dep_id) + \
                                    "</field></row>"

            else: # covering cases for department AGRICULTURE
                degree_types = program_div.find_all('h4')
                for deg in degree_types:
                    degree_type = deg.text.strip().lower()
                    programs= deg.find_next('ul').find_all('li')
                    for prog in programs:
                        count = count + 1
                        xml_program = xml_program + "<row>" + \
                                    "<field name=\"program_id\">" + str(count) + \
                                    "</field><field name=\"program_name\">" + prog.text.strip().replace('&', 'and') + \
                                    "</field><field name=\"program_type\">" + degree_type + \
                                    "</field><field name=\"Department_department_id\">" + str(current_dep_id) + \
                                    "</field></row>"


        elif  current_dep_id and current_dep_id > 4 and current_dep_id < 7: # FACULTY OF ARCHITECTURE AND PLANNING
            
            department_page_link = dep.find('a')['href'] # gets link of the department home page

            if not 'http:' in department_page_link:
                department_page_link = "http://www.dal.ca" + department_page_link.replace('.html', '/programs.html')

            soup = get_soup(department_page_link)

            if current_dep_id == 5: # covers case for school of architecture
                programs = soup.find('div', attrs={'class':'maincontent'}).find_next('ul').find_all('li')
                # print (programs)

                for prog in programs:
                    count = count + 1
                    xml_program = xml_program + "<row>" + \
                                "<field name=\"program_id\">" + str(count) + \
                                "</field><field name=\"program_name\">" + prog.text.strip().replace('&', 'and') + \
                                "</field><field name=\"program_type\">" + degree_type + \
                                "</field><field name=\"Department_department_id\">" + str(current_dep_id) + \
                                "</field></row>"

            if current_dep_id == 6: # covers case for school of planning
                program_divs = soup.find_all('div', attrs={'class':'text parbase section'})
                for prog in program_divs:
                    # print (prog.find('h3'))
                    degree_type=prog.find('h3').text.lower()
                    programs = prog.find_all('b')

                    for p in programs:
                        count = count + 1
                        xml_program = xml_program + "<row>" + \
                                    "<field name=\"program_id\">" + str(count) + \
                                    "</field><field name=\"program_name\">" + p.text.strip().replace('&', 'and') + \
                                    "</field><field name=\"program_type\">" + degree_type + \
                                    "</field><field name=\"Department_department_id\">" + str(current_dep_id) + \
                                    "</field></row>"

        elif  current_dep_id and current_dep_id > 63 and current_dep_id < 74: # FACULTY OF SCIENCE
            department_page_link = dep.find('a')['href'] # gets link of the department home page

            if not 'http:' in department_page_link:
                department_page_link = "http://www.dal.ca" + department_page_link

            soup = get_soup(department_page_link)

            if current_dep_id == 64:
                degree_type = 'undergraduate'
                ug_page_link="https://www.dal.ca/faculty/science/biology/undergraduate.html"
                soup = get_soup(ug_page_link)

                tables = soup.find_all('table')
                for table in tables[1:]:
                    rows = table.find_all('tr')
                    for row in rows[1:]:
                        count = count + 1
                        xml_program = xml_program + "<row>" + \
                                    "<field name=\"program_id\">" + str(count) + \
                                    "</field><field name=\"program_name\">" + row.find_all('td')[0].text.strip().replace('&', 'and') + \
                                    "</field><field name=\"program_type\">" + degree_type + \
                                    "</field><field name=\"Department_department_id\">" + str(current_dep_id) + \
                                    "</field></row>"
                count = count + 1

                xml_program = xml_program + "<row>" + \
                                    "<field name=\"program_id\">" + str(count) + \
                                    "</field><field name=\"program_name\">" + 'MSc in Biology' + \
                                    "</field><field name=\"program_type\">" + 'masters' + \
                                    "</field><field name=\"Department_department_id\">" + str(current_dep_id) + \
                                    "</field></row>"
                count = count + 1

                xml_program = xml_program + "<row>" + \
                                    "<field name=\"program_id\">" + str(count) + \
                                    "</field><field name=\"program_name\">" + 'PhD in Biology' + \
                                    "</field><field name=\"program_type\">" + 'doctorate' + \
                                    "</field><field name=\"Department_department_id\">" + str(current_dep_id) + \
                                    "</field></row>"



                            



    xml_program = xml_program + "</table_data></database>"

    return xml_program        




def scrape_and_build_professor_xml():
    """
    Utility function to fetch professors and build a XML string
    """

    cursor = mydb.cursor()
    cursor.execute("SELECT department_name, department_id FROM department")
    departments_db_dict = dict(cursor.fetchall())
    cursor.execute("SELECT department_id, Faculty_faculty_id FROM department")
    department_faculty_dict = dict(cursor.fetchall())


    url = "https://www.dal.ca/academics/faculties.html"
    soup = get_soup(url)

    departments = soup.find_all('li') # fetches all departments

    xml_professor = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"professor\">"
    count = 0

    for dep in departments:
        current_dep_id = departments_db_dict.get(dep.text.strip().replace('\xa0&', '').replace('&', 'and')) # maintains current department ID in loop
        current_faculty_id = department_faculty_dict.get(current_dep_id) # maintains current faculty ID in loop


        # mocks an API call to coveo API requesting data for professors with different form data for each department

        if current_dep_id and current_dep_id == 1:

            header = {'Authorization': 'Bearer xxdf863a33-5689-4a01-bbee-828fae6c81f5'}
            form_data = 'cq=%40profileexists%3D%3Dtrue%20AND%20%40profiledepartment%3D%3D(%22Dalhousie%20University%7CFaculty%20of%20Agriculture%7CDepartment%20of%20Business%20%26%20Social%20Sciences%22)&numberOfResults=100&fieldsToInclude=%5B%22profileimage%22%2C%22profilefamilyname%22%2C%22profilehonorificprefix%22%2C%22profilegivenname%22%2C%22profilehonorificsuffix%22%2C%22profilejobtitle%22%2C%22profileemail%22%2C%22profiletelephone%22%2C%22profilefaxNumber%22%2C%22profileexists%22%2C%22outlookformacuri%22%2C%22outlookuri%22%2C%22connectortype%22%2C%22urihash%22%2C%22collection%22%2C%22source%22%2C%22author%22%2C%22date%22%2C%22language%22%2C%22objecttype%22%2C%22filetype%22%2C%22permanentid%22%5D&enableDidYouMean=true&sortCriteria=%40profilefamilyname%20ascending%2C%20%40profilegivenname%20ascending&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&groupBy=%5B%7B%22field%22%3A%22%40profiledepartment%22%2C%22maximumNumberOfValues%22%3A10001%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A10000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%5D'

            r = requests.post('https://platform.cloud.coveo.com/rest/search/v2?organizationId=dalhousieuniversityproductionqax94e5b', headers=header, data=form_data)
            records = r.json().get('results')

            for r in records:
                professor_name = r.get('title').split('-')[0].strip().split(' ')
                f_name=professor_name[0]
                l_name='-'.join(professor_name[1:])
                professor_email = r.get('raw').get('profileemail')
                
                count = count + 1
                xml_professor = xml_professor + "<row>" + \
                    "<field name=\"professor_id\">" + str(count) + \
                    "</field><field name=\"professor_first_name\">" + f_name + \
                    "</field><field name=\"professor_last_name\">" + l_name + \
                    "</field><field name=\"professor_email\">" + professor_email + \
                    "</field><field name=\"Faculty_faculty_id\">" + str(current_faculty_id) + \
                    "</field></row>"

        if current_dep_id and current_dep_id == 2:

            header = {'Authorization': 'Bearer xxdf863a33-5689-4a01-bbee-828fae6c81f5'}
            form_data = "actionsHistory=%5B%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A31%3A31.444Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A22%3A54.642Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A19%3A14.534Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A11%3A02.196Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A05%3A37.512Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A00%3A54.367Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A59%3A51.273Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A58%3A25.463Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A53%3A43.348Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T21%3A44%3A56.159Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T21%3A42%3A37.176Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A15%3A19.122Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A14%3A08.516Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A12%3A49.836Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-22T00%3A42%3A54.332Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-21T23%3A04%3A55.873Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-21T22%3A59%3A57.837Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-18T21%3A53%3A01.681Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-18T21%3A51%3A24.094Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-18T01%3A06%3A49.003Z%5C%22%22%7D%5D&referrer=https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fagriculture%2Fengineering%2Ffaculty-staff.html&visitorId=c5139b05-8ac6-4456-9612-2233e93d5b19&isGuestUser=false&cq=%40profileexists%3D%3Dtrue%20AND%20%40profiledepartment%3D%3D(%22Dalhousie%20University%7CFaculty%20of%20Agriculture%7CDepartment%20of%20Engineering%22)&searchHub=default&locale=en&pipeline=profiles&firstResult=0&numberOfResults=100&excerptLength=200&fieldsToInclude=%5B%22profileimage%22%2C%22profilefamilyname%22%2C%22profilehonorificprefix%22%2C%22profilegivenname%22%2C%22profilehonorificsuffix%22%2C%22profilejobtitle%22%2C%22profileemail%22%2C%22profiletelephone%22%2C%22profilefaxNumber%22%2C%22profiledepartmentlinks%22%2C%22profileexists%22%2C%22outlookformacuri%22%2C%22outlookuri%22%2C%22connectortype%22%2C%22urihash%22%2C%22collection%22%2C%22source%22%2C%22author%22%2C%22date%22%2C%22language%22%2C%22objecttype%22%2C%22filetype%22%2C%22permanentid%22%5D&enableDidYouMean=true&sortCriteria=%40profilefamilyname%20ascending%2C%20%40profilegivenname%20ascending&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&groupBy=%5B%7B%22field%22%3A%22%40profiledepartment%22%2C%22maximumNumberOfValues%22%3A10001%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A10000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%5D&categoryFacets=%5B%5D&retrieveFirstSentences=true&timezone=Asia%2FCalcutta&enableQuerySyntax=false&enableDuplicateFiltering=false&enableCollaborativeRating=false&debug=false&allowQueriesWithoutKeywords=true"
            r = requests.post('https://platform.cloud.coveo.com/rest/search/v2?organizationId=dalhousieuniversityproductionqax94e5b', headers=header, data=form_data)

            records = r.json().get('results')

            for r in records:
                professor_name = r.get('title').split('-')[0].strip().split(' ')
                f_name=professor_name[0]
                l_name='-'.join(professor_name[1:])
                professor_email = r.get('raw').get('profileemail')
                
                count = count + 1
                xml_professor = xml_professor + "<row>" + \
                    "<field name=\"professor_id\">" + str(count) + \
                    "</field><field name=\"professor_first_name\">" + f_name + \
                    "</field><field name=\"professor_last_name\">" + l_name + \
                    "</field><field name=\"professor_email\">" + professor_email + \
                    "</field><field name=\"Faculty_faculty_id\">" + str(current_faculty_id) + \
                    "</field></row>"

        if current_dep_id and current_dep_id == 3:

            header = {'Authorization': 'Bearer xxdf863a33-5689-4a01-bbee-828fae6c81f5'}
            form_data = "actionsHistory=%5B%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A16%3A47.613Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A11%3A49.228Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A56%3A11.934Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A54%3A28.394Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A48%3A48.985Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A31%3A31.444Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A22%3A54.642Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A19%3A14.534Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A11%3A02.196Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A05%3A37.512Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A00%3A54.367Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A59%3A51.273Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A58%3A25.463Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A53%3A43.348Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T21%3A44%3A56.159Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T21%3A42%3A37.176Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A15%3A19.122Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A14%3A08.516Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A12%3A49.836Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-22T00%3A42%3A54.332Z%5C%22%22%7D%5D&referrer=https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fagriculture%2Fplant-food-env%2Ffaculty-staff.html&visitorId=c5139b05-8ac6-4456-9612-2233e93d5b19&isGuestUser=false&cq=%40profileexists%3D%3Dtrue%20AND%20%40profiledepartment%3D%3D(%22Dalhousie%20University%7CFaculty%20of%20Agriculture%7CDepartment%20of%20Plant%2C%20Food%2C%20and%20Environmental%20Sciences%22)%20AND%20%40profiletype%3D%3Dfaculty&searchHub=default&locale=en&pipeline=profiles&firstResult=0&numberOfResults=10&excerptLength=200&fieldsToInclude=%5B%22profileimage%22%2C%22profilefamilyname%22%2C%22profilehonorificprefix%22%2C%22profilegivenname%22%2C%22profilehonorificsuffix%22%2C%22profilejobtitle%22%2C%22profileemail%22%2C%22profiletelephone%22%2C%22profilefaxNumber%22%2C%22profiledepartmentlinks%22%2C%22profileexists%22%2C%22outlookformacuri%22%2C%22outlookuri%22%2C%22connectortype%22%2C%22urihash%22%2C%22collection%22%2C%22source%22%2C%22author%22%2C%22date%22%2C%22language%22%2C%22objecttype%22%2C%22filetype%22%2C%22permanentid%22%5D&enableDidYouMean=true&sortCriteria=%40profilefamilyname%20ascending%2C%20%40profilegivenname%20ascending&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&groupBy=%5B%7B%22field%22%3A%22%40profiledepartment%22%2C%22maximumNumberOfValues%22%3A10001%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A10000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%5D&categoryFacets=%5B%5D&retrieveFirstSentences=true&timezone=Asia%2FCalcutta&enableQuerySyntax=false&enableDuplicateFiltering=false&enableCollaborativeRating=false&debug=false&allowQueriesWithoutKeywords=true"
            r = requests.post('https://platform.cloud.coveo.com/rest/search/v2?organizationId=dalhousieuniversityproductionqax94e5b', headers=header, data=form_data)

            records = r.json().get('results')

            for r in records:
                professor_name = r.get('title').split('-')[0].strip().split(' ')
                f_name=professor_name[0]
                l_name='-'.join(professor_name[1:])
                professor_email = r.get('raw').get('profileemail')
                
                count = count + 1
                xml_professor = xml_professor + "<row>" + \
                    "<field name=\"professor_id\">" + str(count) + \
                    "</field><field name=\"professor_first_name\">" + f_name + \
                    "</field><field name=\"professor_last_name\">" + l_name + \
                    "</field><field name=\"professor_email\">" + professor_email + \
                    "</field><field name=\"Faculty_faculty_id\">" + str(current_faculty_id) + \
                    "</field></row>"

        if current_dep_id and current_dep_id == 4:

            header = {'Authorization': 'Bearer xxdf863a33-5689-4a01-bbee-828fae6c81f5'}
            form_data =  "actionsHistory=%5B%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A19%3A52.555Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A16%3A47.613Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A11%3A49.228Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A56%3A11.934Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A54%3A28.394Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A48%3A48.985Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A31%3A31.444Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A22%3A54.642Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A19%3A14.534Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A11%3A02.196Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A05%3A37.512Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A00%3A54.367Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A59%3A51.273Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A58%3A25.463Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A53%3A43.348Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T21%3A44%3A56.159Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T21%3A42%3A37.176Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A15%3A19.122Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A14%3A08.516Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A12%3A49.836Z%5C%22%22%7D%5D&referrer=https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fagriculture%2Fanimal-science-aquaculture%2Ffaculty-staff.html&visitorId=c5139b05-8ac6-4456-9612-2233e93d5b19&isGuestUser=false&cq=%40profileexists%3D%3Dtrue%20AND%20%40profiledepartment%3D%3D(%22Dalhousie%20University%7CFaculty%20of%20Agriculture%7CDepartment%20of%20Animal%20Science%20and%20Aquaculture%22)&searchHub=default&locale=en&pipeline=profiles&firstResult=0&numberOfResults=100&excerptLength=200&fieldsToInclude=%5B%22profileimage%22%2C%22profilefamilyname%22%2C%22profilehonorificprefix%22%2C%22profilegivenname%22%2C%22profilehonorificsuffix%22%2C%22profilejobtitle%22%2C%22profileemail%22%2C%22profiletelephone%22%2C%22profilefaxNumber%22%2C%22profiledepartmentlinks%22%2C%22profileexists%22%2C%22outlookformacuri%22%2C%22outlookuri%22%2C%22connectortype%22%2C%22urihash%22%2C%22collection%22%2C%22source%22%2C%22author%22%2C%22date%22%2C%22language%22%2C%22objecttype%22%2C%22filetype%22%2C%22permanentid%22%5D&enableDidYouMean=true&sortCriteria=%40profilefamilyname%20ascending%2C%20%40profilegivenname%20ascending&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&groupBy=%5B%7B%22field%22%3A%22%40profiledepartment%22%2C%22maximumNumberOfValues%22%3A10001%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A10000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%5D&categoryFacets=%5B%5D&retrieveFirstSentences=true&timezone=Asia%2FCalcutta&enableQuerySyntax=false&enableDuplicateFiltering=false&enableCollaborativeRating=false&debug=false&allowQueriesWithoutKeywords=true"
            r = requests.post('https://platform.cloud.coveo.com/rest/search/v2?organizationId=dalhousieuniversityproductionqax94e5b', headers=header, data=form_data)

            records = r.json().get('results')

            for r in records:
                professor_name = r.get('title').split('-')[0].strip().split(' ')
                f_name=professor_name[0]
                l_name='-'.join(professor_name[1:])
                professor_email = r.get('raw').get('profileemail')
                
                count = count + 1
                xml_professor = xml_professor + "<row>" + \
                    "<field name=\"professor_id\">" + str(count) + \
                    "</field><field name=\"professor_first_name\">" + f_name + \
                    "</field><field name=\"professor_last_name\">" + l_name + \
                    "</field><field name=\"professor_email\">" + professor_email + \
                    "</field><field name=\"Faculty_faculty_id\">" + str(current_faculty_id) + \
                    "</field></row>"

        if current_dep_id and current_dep_id == 5:

            header = {'Authorization': 'Bearer xxdf863a33-5689-4a01-bbee-828fae6c81f5'}
            form_data = "actionsHistory=%5B%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A26%3A35.351Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A19%3A52.555Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A16%3A47.613Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A11%3A49.228Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A56%3A11.934Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A54%3A28.394Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A48%3A48.985Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A31%3A31.444Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A22%3A54.642Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A19%3A14.534Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A11%3A02.196Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A05%3A37.512Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A00%3A54.367Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A59%3A51.273Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A58%3A25.463Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A53%3A43.348Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T21%3A44%3A56.159Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T21%3A42%3A37.176Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A15%3A19.122Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A14%3A08.516Z%5C%22%22%7D%5D&referrer=https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Farchitecture-planning%2Fschool-of-architecture%2Fprograms.html&visitorId=c5139b05-8ac6-4456-9612-2233e93d5b19&isGuestUser=false&cq=%40profileexists%3D%3Dtrue%20AND%20%40profiledepartment%3D%3D(%22Dalhousie%20University%7CFaculty%20of%20Architecture%20and%20Planning%7CSchool%20of%20Architecture%22)&searchHub=default&locale=en&pipeline=profiles&firstResult=0&numberOfResults=100&excerptLength=200&fieldsToInclude=%5B%22profileimage%22%2C%22profilefamilyname%22%2C%22profilehonorificprefix%22%2C%22profilegivenname%22%2C%22profilehonorificsuffix%22%2C%22profilejobtitle%22%2C%22profileemail%22%2C%22profiletelephone%22%2C%22profilefaxNumber%22%2C%22profiledepartmentlinks%22%2C%22profileexists%22%2C%22outlookformacuri%22%2C%22outlookuri%22%2C%22connectortype%22%2C%22urihash%22%2C%22collection%22%2C%22source%22%2C%22author%22%2C%22date%22%2C%22language%22%2C%22objecttype%22%2C%22filetype%22%2C%22permanentid%22%5D&enableDidYouMean=true&sortCriteria=%40profilefamilyname%20ascending%2C%20%40profilegivenname%20ascending&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&groupBy=%5B%7B%22field%22%3A%22%40profiledepartment%22%2C%22maximumNumberOfValues%22%3A10001%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A10000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%5D&categoryFacets=%5B%5D&retrieveFirstSentences=true&timezone=Asia%2FCalcutta&enableQuerySyntax=false&enableDuplicateFiltering=false&enableCollaborativeRating=false&debug=false&allowQueriesWithoutKeywords=true"
            r = requests.post('https://platform.cloud.coveo.com/rest/search/v2?organizationId=dalhousieuniversityproductionqax94e5b', headers=header, data=form_data)

            records = r.json().get('results')

            for r in records:
                professor_name = r.get('title').split('-')[0].strip().split(' ')
                f_name=professor_name[0]
                l_name='-'.join(professor_name[1:])
                professor_email = r.get('raw').get('profileemail')
                
                count = count + 1
                xml_professor = xml_professor + "<row>" + \
                    "<field name=\"professor_id\">" + str(count) + \
                    "</field><field name=\"professor_first_name\">" + f_name + \
                    "</field><field name=\"professor_last_name\">" + l_name + \
                    "</field><field name=\"professor_email\">" + professor_email + \
                    "</field><field name=\"Faculty_faculty_id\">" + str(current_faculty_id) + \
                    "</field></row>"

        if current_dep_id and current_dep_id == 6:

            soup = get_soup('https://www.dal.ca/faculty/architecture-planning/school-of-planning/People/People.html')
            records = soup.find('div', attrs={'class':'text parbase section'}).find_next('table').find_all('tr')

            for r in records:
                if not r.find_all('h3'):
                    professor_name = r.find_all('td')[0].text.strip().replace('&', 'and').split(' ')
                    professor_email = r.find_all('td')[1].text.strip().replace('&', 'and')
                    if professor_name and professor_email:
                        f_name=professor_name[0]
                        l_name='-'.join(professor_name[1:])
                        count = count + 1
                        xml_professor = xml_professor + "<row>" + \
                            "<field name=\"professor_id\">" + str(count) + \
                            "</field><field name=\"professor_first_name\">" + f_name + \
                            "</field><field name=\"professor_last_name\">" + l_name + \
                            "</field><field name=\"professor_email\">" + professor_email + \
                            "</field><field name=\"Faculty_faculty_id\">" + str(current_faculty_id) + \
                            "</field></row>"


        if current_dep_id and current_dep_id == 64:

            header = {'Authorization': 'Bearer xxdf863a33-5689-4a01-bbee-828fae6c81f5'}
            form_data = "actionsHistory=%5B%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A29%3A37.564Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A26%3A35.351Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A19%3A52.555Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A16%3A47.613Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T02%3A11%3A49.228Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A56%3A11.934Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A54%3A28.394Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A48%3A48.985Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-25T00%3A31%3A31.444Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A22%3A54.642Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A19%3A14.534Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A11%3A02.196Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A05%3A37.512Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T15%3A00%3A54.367Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A59%3A51.273Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A58%3A25.463Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-24T14%3A53%3A43.348Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T21%3A44%3A56.159Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T21%3A42%3A37.176Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22time%22%3A%22%5C%222019-09-23T14%3A15%3A19.122Z%5C%22%22%7D%5D&referrer=https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology.html&visitorId=c5139b05-8ac6-4456-9612-2233e93d5b19&isGuestUser=false&cq=%40profileexists%3D%3Dtrue%20AND%20(%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fpaul-bentzen.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Ferin-bertrand.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fjoe-bielawski.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fpatrice-cote.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fglenn-crossin.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Farunika-gunawardena.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fchristophe-herbinger.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fjeffrey-hutchings.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fsara-iverson.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fmark-johnston.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fpatricia-lane.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fjulie-laroche.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Frobert-latta.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fmarty-leonard.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fheike-lotze.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Faaron-macneil.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fdaniel-ruzzante.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Falastair-simpson.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fsophia-stone.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fderek-tittensor.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fsandra-walde.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fboris-worm.html'%20OR%20%40uri%3D%3D'https%3A%2F%2Fwww.dal.ca%2Ffaculty%2Fscience%2Fbiology%2Ffaculty-staff%2Four-faculty%2Fhal-whitehead.html')&searchHub=default&locale=en&pipeline=profiles&firstResult=0&numberOfResults=100&excerptLength=200&fieldsToInclude=%5B%22profileimage%22%2C%22profilefamilyname%22%2C%22profilehonorificprefix%22%2C%22profilegivenname%22%2C%22profilehonorificsuffix%22%2C%22profilejobtitle%22%2C%22profileemail%22%2C%22profiletelephone%22%2C%22profilefaxNumber%22%2C%22profileexists%22%2C%22outlookformacuri%22%2C%22outlookuri%22%2C%22connectortype%22%2C%22urihash%22%2C%22collection%22%2C%22source%22%2C%22author%22%2C%22date%22%2C%22language%22%2C%22objecttype%22%2C%22filetype%22%2C%22permanentid%22%5D&enableDidYouMean=true&sortCriteria=%40profilefamilyname%20ascending%2C%20%40profilegivenname%20ascending&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&groupBy=%5B%7B%22field%22%3A%22%40profiledepartment%22%2C%22maximumNumberOfValues%22%3A10001%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A10000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%5D&categoryFacets=%5B%5D&retrieveFirstSentences=true&timezone=Asia%2FCalcutta&enableQuerySyntax=false&enableDuplicateFiltering=false&enableCollaborativeRating=false&debug=false&allowQueriesWithoutKeywords=true"
            r = requests.post('https://platform.cloud.coveo.com/rest/search/v2?organizationId=dalhousieuniversityproductionqax94e5b', headers=header, data=form_data)

            records = r.json().get('results')

            for r in records:
                professor_name = r.get('title').split('-')[0].strip().split(' ')
                f_name=professor_name[0]
                l_name='-'.join(professor_name[1:])
                professor_email = r.get('raw').get('profileemail')
                # print (f_name, l_name)                
                count = count + 1
                xml_professor = xml_professor + "<row>" + \
                    "<field name=\"professor_id\">" + str(count) + \
                    "</field><field name=\"professor_first_name\">" + f_name + \
                    "</field><field name=\"professor_last_name\">" + l_name + \
                    "</field><field name=\"professor_email\">" + professor_email + \
                    "</field><field name=\"Faculty_faculty_id\">" + str(current_faculty_id) + \
                    "</field></row>"


    xml_professor = xml_professor + "</table_data></database>"

    return xml_professor 



def scrape_and_build_funding_sources_xml():
    """
    Utility function that makes XML string for four tables, research; internal; external; awards
    """
    soup = get_soup('https://www.dal.ca/dept/research-services/opportunities.html')
    xml_researchoffice = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"researchoffice\">"
    xml_researchoffice = xml_researchoffice + "<row>" + \
                    "<field name=\"office_id\">" + '1' + \
                    "</field><field name=\"office_name\">" + soup.find_all('h2')[1].text.strip() + \
                    "</field></row>"
    xml_researchoffice = xml_researchoffice + "</table_data></database>"


    xml_internalfunding = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"internalfunding\">"
    xml_externalfunding = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"externalfunding\">"
    xml_awardsandprizes = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"awardsandprizes\">"

    soup_internal = get_soup('https://www.dal.ca/dept/research-services/opportunities/internal-funding.html')
    soup_external = get_soup('https://www.dal.ca/dept/research-services/opportunities/external-funding.html')
    soup_awardsandprizes = get_soup('https://www.dal.ca/dept/research-services/opportunities/nominations-and-prizes.html')


    internal_grants = soup_internal.find_all('h4')

    for i, g in enumerate(internal_grants):
        if not 'How and when' in g.text and not 'Notification of the award' in g.text:
            xml_internalfunding = xml_internalfunding + '<row>' + \
                            "<field name=\"id\">" + str(i) + \
                            "</field><field name=\"type_of_grant\">" + g.text.strip().replace('&', 'and') + \
                            "</field><field name=\"ResearchOffice_office_id\">" + '1' + \
                            "</field></row>"
    xml_internalfunding = xml_internalfunding + "</table_data></database>"



    external_grants = soup_external.find('div', attrs={'class':'text parbase section'}).find_all('li')

    for i, g in enumerate(external_grants):
        if not 'How and when' in g.text and not 'Notification of the award' in g.text:
            xml_externalfunding = xml_externalfunding + '<row>' + \
                            "<field name=\"id\">" + str(i) + \
                            "</field><field name=\"type_of_grant\">" + g.text.strip().replace('&', 'and') + \
                            "</field><field name=\"ResearchOffice_office_id\">" + '1' + \
                            "</field></row>"
    xml_externalfunding = xml_externalfunding + "</table_data></database>"



    awardsandprizes = soup_awardsandprizes.find('div', attrs={'class':'maincontent'}).find_next('table').find_all('tr')

    for i, g in enumerate(awardsandprizes[1:]):
        if not 'How and when' in g.text and not 'Notification of the award' in g.text:
            xml_awardsandprizes = xml_awardsandprizes + '<row>' + \
                            "<field name=\"id\">" + str(i) + \
                            "</field><field name=\"type_of_grant\">" + g.find_all('td')[0].text.strip().replace('&', 'and') + \
                            "</field><field name=\"ResearchOffice_office_id\">" + '1' + \
                            "</field></row>"
    xml_awardsandprizes = xml_awardsandprizes + "</table_data></database>"

    return xml_researchoffice, xml_internalfunding, xml_externalfunding, xml_awardsandprizes


def build_facility_and_facility_xml():
    xml_facilitytype = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"facilitytype\">"
    xml_facilitysubtype = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"facilitysubtype\">"

    facility_dict = {'dalplex': ["badminton", "swimming", "basketball", "climbing", "personal training", "squash"],
                    'residence': ["gerard hall", "mini res", "shireff hall", "howe hall", "risley hall", "le marchant place", "glengary apartment", "graduate house"],
                    'library': ["Killam Library", "Sexton Library", "MacRae Library", "Kellog Library"],
                    'international_centre':[]}

    count = 0
    facility_type = facility_dict.keys()
    for i, f in enumerate(facility_type):
        xml_facilitytype = xml_facilitytype + '<row>' + \
                            "<field name=\"facility_id\">" + str(i) + \
                            "</field><field name=\"facility_name\">" + str(f) + \
                            "</field></row>"

        for x in facility_dict.get(f):
            count += 1
            xml_facilitysubtype = xml_facilitysubtype + '<row>' + \
                                "<field name=\"id\">" + str(count) + \
                                "</field><field name=\"facility_subtype\">" + str(x) + \
                                "</field><field name=\"FacilityType_facility_id\">" + str(i) + \
                                "</field></row>"
    xml_facilitytype = xml_facilitytype + "</table_data></database>"
    xml_facilitysubtype = xml_facilitysubtype + "</table_data></database>"

    return xml_facilitytype, xml_facilitysubtype


xml_facilitytype, xml_facilitysubtype = build_facility_and_facility_xml()



def build_campus_xml():
    """
    builds a dummy xml for campus
    """
    campus_list = ['studley', 'sexton', 'carleton', 'truro']
    xml_campus = "<?xml version=\"1.0\"?><database name=\"assignment1b\"><table_data name=\"campus\">"

    for i, c in enumerate(campus_list):
        xml_campus = xml_campus + "<row>" + \
                            "<field name=\"campus_id\">" + str(i) + \
                            "</field><field name=\"campus_name\">" + c.strip() + \
                            "</field></row>"

    xml_campus = xml_campus + "</table_data></database>"
    return xml_campus


#carleton sexton truro studley
# scrape_and_build_funding_sources_xml()

f = open("C:\\Users\\rahul\\Desktop\\Faculty.xml", 'w+', encoding='utf-8')
f.write(build_xml_faculty())
f.close()




