import requests
import json
import csv

session = requests.Session()


HEADER_FIELDS = [
    'Job Title',
    'Date Posted',
    'Link to Job',
    'Location',
    'Description & Basic Qualifications & Preferred Qualifications'
]

pageIdx = 500
perCount = 1
with open('amazon-jobs.csv', 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=HEADER_FIELDS)
    csv_writer.writeheader()

    while True:
        url = 'https://www.amazon.jobs/en/search.json?base_query=&business_category[]=alexa&city=&country=&county=&facets[]=location&facets[]=business_category&facets[]=category&facets[]=schedule_type_id&facets[]=employee_class&facets[]=normalized_location&facets[]=job_function_id&latitude=&loc_group_id=&loc_query=&longitude=&offset=%s&query_options=&radius=24km&region=&result_limit=%s&sort=relevant' % (
            (pageIdx-1)*perCount, perCount)

        response = session.get(url)

        if response.status_code == 200:
            jobs = json.loads(response.text.encode('utf8'))['jobs']

            if len(jobs):
                for _job in jobs:
                    job_description = '\n'.join(['DESCRIPTION', _job['description'], '\n\nBASIC QUALIFICATIONS',
                                                 _job['basic_qualifications'], '\n\nPREFERRED QUALIFICATIONS', _job['preferred_qualifications']])

                    job_description = job_description.replace('<br/>', '\n')
                    job = {
                        'Job Title': _job['title'],
                        'Date Posted': _job['posted_date'],
                        'Link to Job': 'https://www.amazon.jobs' + _job['job_path'],
                        'Location': _job['location'],
                        'Description & Basic Qualifications & Preferred Qualifications': job_description
                    }

                    print(job)
                    csv_writer.writerow(job)

                pageIdx += 1
            else:
                break
        else:
            break
