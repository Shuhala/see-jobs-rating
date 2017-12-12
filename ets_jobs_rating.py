import requests
import json
import re
import time

# Settings
file_input = 'SEE_jobs.json'
file_output = 'SEE_rating.txt'
api_token = ''
api_token_key = ''

# Config
api_url_base = 'http://api.glassdoor.com/api/api.htm'
headers = {"Content-Type": "application/x-www-form-urlencoded", "user-agent": "Mozilla/5.0"}
parameters = {
    "t.p": api_token,
    "t.k": api_token_key,
    "userip": "0.0.0.0",
    "format": "json",
    "v": 1,
    "action": "employers"
}
data = json.load(open(file_input))
errors = {}
companies_not_found = []
jobs = []


def normalize(name):
    # https://docs.python.org/2/library/string.html#string.maketrans
    translation = str.maketrans("éàèùâêîôûç", "eaeuaeiouc")
    name = name.translate(translation) \
        .lower() \
        .split("-")[0] \
        .split("–")[0] \
        .split(",")[0]
    return re.sub('(\([^]]*\)\s?)|&|\+|inc|INC|\.', '', name)


# Fetch data
with open(file_output, 'w') as file:
    for d in data:
        company_name = normalize(d['Nmemp'])
        parameters["q"] = company_name
        parameters["l"] = d['Lieupost']

        # Don't try to fetch companies if they already failed once
        if company_name not in companies_not_found or company_name not in errors.keys():
            print(company_name)
            response = requests.get(api_url_base, params=parameters, headers=headers).json()
            time.sleep(0.2)

            try:
                if response and response['response']['employers']:
                    employers = sorted(response['response']['employers'], key=lambda k: k['overallRating'], reverse=True)
                    jobs.append({
                        "name": d['Nmemp'],
                        "job_title": d['Titpost'],
                        "glassdoor": employers,
                        "top_rating": employers[0]['overallRating']
                    })
                else:
                    companies_not_found.append(company_name)
            except Exception as E:
                errors.update({company_name: str(response)})

    # Successful results
    file.write("\n%-140s %-100s\n" % ('ETS', 'TOP GLASSDOOR RESULT'))
    file.write("%-40s %-100s %-10s %-10s %-10s %-50s %-50s\n\n" % ('Company', 'Job title', 'rating', '# ratings', '# results', 'Company', 'Website'))
    for res in [r for r in sorted(jobs, key=lambda k: k['top_rating'], reverse=True)]:
        file.write("%-40s %-100s %-10s %-10s %-10s %-50s %-50s\n" %
                   (
                       res['name'],
                       res['job_title'],
                       res['glassdoor'][0]['overallRating'],
                       res['glassdoor'][0]['numberOfRatings'],
                       len(res['glassdoor']),
                       res['glassdoor'][0]['name'],
                       res['glassdoor'][0]['website'])
                   )

    # Companies not found
    file.write("\n\n -- Not found -- \n")
    for job_company_name in companies_not_found:
        file.write("\n %s" % job_company_name)

    # Errors
    file.write("\n\n\n -- Errors -- \n")
    for company_name, error in errors.items():
        file.write("\n %s -> %s" % (company_name, error))

print('Done!')
