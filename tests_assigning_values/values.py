import numpy as np
import scipy as sci
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

skills = {
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
            'intro_extro': p['intro_extro'] / 100.,
            'soft_hard_learn': p['soft_hard_learn'] / 100.,
            'skills_learn': [skills.get(str(x).lower()) for x in p['skills_learn']],
            'soft_hard_already': p['soft_hard_already'] / 100.,
            'skills_already': [skills.get(str(x).lower()) for x in p['skills_already']],
            'skills_project_general': [skills.get(str(x).lower()) for x in p['skills_project_general']],
            'skills_project_needed': [skills.get(str(x).lower()) for x in p['skills_project_needed']],
        })
        print(company)
        print('success')
        
def dist(a,b,length):
    return min(abs(a-b), 15 - abs(a-b))


# defining weight factors
factors ={
    'ment_supp': -1,
    'overwhelmed': -1,
    'anxiety': -1,
    'trust': -1,
    'friendship': -1,
    'help': -1,
    'advice': -1,
    'sleep': -0.5,
    'exercise': -1,
    'hobbies': 1,
    'comp_exp': -1,
    'field_exp': -1,
    'programming_lan': 1,
    'intro_extro': -1,
    'soft_hard_learn': 1,
    'skills_learn': 1,
    'soft_hard_already': 1,
    'skills_already': 1,
    'skills_project_general': 1,
    'skills_project_needed': 1,
}

critical = ['hobbies','programming_lan','skills_learn','skills_already','skills_project_general','skills_project_needed', 'soft_hard_learn','soft_hard_already']



#____________DEFINING THE COEFFICIENT MATRICES_______________
# Defining a correlation matrix based on the entries in the skill dictionary
def skill_matrix(skill_dict):
    dim = len(skill_dict)
    mat = np.zeros((dim,dim))
    for i in range(0,dim):
        for j in range(i,dim):
            mat[i,j] = mat[j,i] = 1./(2**(min(j-i, dim - (j-i))))
    return mat



def hobby_matrix(hobby_dict):
    dim = len(hobby_dict)
    mat1 = np.zeros((dim,dim))
    for i in range(0,dim):
        for j in range(i,dim):
            mat1[i,j] = mat1[j,i] = 1./(2**(min(j-i, dim - (j-i))))
    mat2 = np.identity(dim)
    count = 0
    for x in hobby_dict:
        if x['frequency'] == 0:
            mat2[count,count] = 1
        else:
            mat2[count,count] = 1. / np.sqrt(x['frequency'])
        count += 1
    
    return mat1 * mat2








vec_factors = np.array([])

# Generating a vector from the factors given by the factors dictionary
def gen_vec(user):
    for feat in user['features']:
        # if feat == 'hobbies' or feat == 'programming_lan' or feat == 'skills_learn' or feat == 'skills_already':
        if user['features'].has_key(feat):
            np.append(vec_factors, factors[feat])
        else:
            np.append(vec_factors,1)

existing_matrix = np.genfromtxt('mat.csv', delimiter=',')

def gen_matrix():
    factor_matrix = np.diag(vec_factors)


# generating a numpy vector depending on the elements from the dictionary
def gen_user_vec(user_dict):
    user = np.array([])
    for feat in user_dict['features']:
        if feat in critical:
            np.append(user,0) # append 0 for the critical list objects within the dictionary
        else:
            np.append(user,user_dict[feat])

    return user


# generating the matching factor contributions for the critical objects
def critical_factors(user1, user2):
    user1_hobbies = np.array(user1['hobbies'])
    user2_hobbies = np.array(user2['hobbies'])
    user1_skills_learn = np.array(user1['skills_learn'])
    user1_skills_already = np.array(user1['skills_already'])
    user2_skills_learn = np.array(user2['skills_learn'])
    user2_skills_already = np.array(user2['skills_already'])


    skills_contribution = user1_hobbies.T * hobby_matrix(hobby_dict) * user2_hobbies
    hobby_contribution = (user1_skills_learn.T * skill_matrix(skill_dict) * user2_skills_already + user2_skills_learn.T * skill_matrix(skill_dict) * user1_skills_already) / 2.
    soft_hard_contribution = (np.array(user1['soft_hard_learn']).T * np.array(user2['soft_hard_already']) + np.array(user2['soft_hard_learn']).T * np.array(user1['soft_hard_already'])) / 2.
    project_contribution = ( np.array(user1['skills_already']).T * np.array(user2['skills_project_needed']) + np.array(user2['skills_already']).T * np.array(user1['skills_project_needed']) ) / 2.

    return skills_contribution + hobby_contribution + soft_hard_contribution + project_contribution

    

# Generating the matching factor for each user combination
def matching_factor(id1,id2):
    user1 = gen_user_vec(users.get(id1))
    user2 = gen_user_vec(users.get(id2))
    factor = sci.spatial.distance.cosine(user1,user2,factors.values())
    factor += critical_factors(users.get(id1), users.get(id2))
    return factor


# Adding a new user to an existing matrix
def new_user(user):
    n = len(existing_matrix[0,:])
    new_matrix = np.hstack((existing_matrix, np.atleast_2d(np.zeros(n)).T))   
    new_matrix = np.vstack((new_matrix, np.atleast_2d(np.zeros(n+1))))

    for i in range(0,n):
        coefficient = matching_factor(i,n)
        new_matrix[i,n] = coefficient
        new_matrix[n,i] = coefficient

    np.savetxt("mat.csv",new_matrix, delimiter=',')  



