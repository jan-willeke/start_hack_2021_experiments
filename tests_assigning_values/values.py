import numpy as np
import json

# creating test json-file
test = {}
test['employee'] = []
test['employee'].append({
    'mental support': 70,
    'overwhelmed': 50,
    'anxiety': 3,
    'trust': 90,
    'friendship':60,
    'help':70,
    'advice': 80,
    'sleep': 4,
    'exercise': 1,
    'hobbies': ['programming','reading','gaming'],
    'comp_experience': 10,
    'field_exp': 15,
    'programming_lan': ['python','cpp','html','latex']
})
with open('data.json','w') as outfile:
    json.dump(test,outfile)


company = {}
company['employees'] = []

hobbies = {
    "programming": 0,
    "reading": 1,
    "outdoor sports": 2,
    "indoor sports": 3,
    "writing": 4,
    "board games": 5,
    "cooking": 6,
    "video editing": 7,
    "painting": 8,
    "gaming": 9,
    "meditating": 10,
    "collecting": 11,
}

lan = {
    'python': 0,
    'cpp': 1,
    'java': 2,
    'julia': 3,
    'r': 4,
    'html': 5,
    'css': 6,
    'c': 7,
    'c_sharp': 8,
    'fortran': 9,
    'pascal': 10,
    'php': 11,
    'latex': 12,
}

with open('data.json') as json_file:
    data = json.load(json_file)
    for p in data['employee']:
        company['employees'].append({
            'ment_supp': p['mental support'] / 100.,
            'overwhelmed': p['overwhelmed'] / 100.,
            'anxiety': p['anxiety'] / 100.,
            'trust': p['trust'] / 100.,
            'friendship': p['friendship'] / 100.,
            'help': p['help'] / 100.,
            'advice': p['advice'] / 100.,
            'sleep': p['sleep'] / 10.,
            'exercise': p['exercise'] / 4.,
            'hobbies': [hobbies.get(str(x)) for x in p['hobbies']],
            'comp_exp': p['comp_experience'] / 50.,
            'field_exp': p['field_exp'] / 50.,
            'programming_lan': [lan.get(str(x)) for x in p['programming_lan']],
        })
        print(company)
        print('success')
        
