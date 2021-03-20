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
    "gaming": 1,
    "board games": 2,
    "reading": 3,
    "painting": 4,
    "writing": 5,
    "meditating": 6,
    "collecting": 7,
    "cooking": 8,
    "outdoor sports": 9,
    "indoor sports": 10,
    "video editing": 11,
}

lan = {
    'r': 0,
    'python': 1,
    'julia': 2,
    'cpp': 3,
    'c': 4,
    'c_sharp': 5,
    'java': 6,
    'fortran': 7,
    'pascal': 8,
    'html': 9,
    'php': 10,
    'latex': 11,
    'css': 12,
}

skills ={
    "communication": 0,
    "interpersonal": 1,
    "empathy": 2,
    "creativity": 3,
    "teamwork": 4,
    "open_mind": 5,
    "ui_ux": 6,
    "programming": 7,
    "critical_thinking": 8,
    "research": 9,
    "adaptability": 10,
    "marketing": 11,
    "leadership": 12,
    "management": 13,
    "team_building": 14,
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
            'hobbies': [hobbies.get(str(x).lower()) for x in p['hobbies']],
            'comp_exp': p['comp_experience'] / 50.,
            'field_exp': p['field_exp'] / 50.,
            'programming_lan': [lan.get(str(x).lower()) for x in p['programming_lan']],
            'intro_extro': p['intro_extro'] / 100,
            'soft_hard_learn': p['soft_hard_learn'] / 100,
            'skills_learn': [skills.get(str(x).lower()) for x in p['skills_learn']],
            'soft_hard_already': p['soft_hard_already'] / 100,
            'skills_already': [skills.get(str(x).lower()) for x in p['skills_already']],
            'skills_project_general': [skills.get(str(x).lower()) for x in p['skills_project_general']],
            'skills_project_needed': [skills.get(str(x).lower()) for x in p['skills_project_needed']],
        })
        print(company)
        print('success')
        
def dist(a,b,length):
    return min(abs(a-b), 15 - abs(a-b))