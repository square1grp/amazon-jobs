import json
import csv

HEADER_FIELDS = [
    'Job Title',
    'Date Posted',
    'Link to Job',
    'Location',
    'Description & Basic Qualifications & Preferred Qualifications'
]

with open('amazon-jobs.csv', 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=HEADER_FIELDS)
    csv_writer.writeheader()

    with open('search.json', 'r') as f:
        jobs = json.loads(f.read())['jobs']

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
