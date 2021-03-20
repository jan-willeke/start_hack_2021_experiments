import numpy as np
import scipy.spatial.distance as sci
import json
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm

users = [
    {
        "id": 1,
        "name": "John Smith",
        "email": "john@example.com",
        "ment_supp": 0.8,
        "overwhelmed": 0.4,
        "anxiety": 0.5,
        "trust": 0.6,
        "friendship": 0.2,
        "help": 0.1,
        "advice": 0.7,
        "sleep": 1.0,
        "exercise": 0.6,
        "comp_exp": 0.7,
        "field_exp": 0.6,
        "intro_extro": 1.0,
        "soft_hard_learn": 0.8,
        "soft_hard_already": 0.3,
        "skills_to_learn": [
            2,
            4
        ],
        "skills_already": [
            3,
            5
        ],
        "hobbies": [
            1,
            2
        ],
        "prog_langs": [
            1,
            3,
            5,
            6
        ]
    },
    {
        "id": 2,
        "name": "John Smith The Second",
        "email": "john@example.com",
        "ment_supp": 0.8,
        "overwhelmed": 0.4,
        "anxiety": 0.5,
        "trust": 0.6,
        "friendship": 0.2,
        "help": 0.1,
        "advice": 0.7,
        "sleep": 1.0,
        "exercise": 0.6,
        "comp_exp": 0.7,
        "field_exp": 0.6,
        "intro_extro": 1.0,
        "soft_hard_learn": 0.8,
        "soft_hard_already": 0.3,
        "skills_to_learn": [
            2,
            4
        ],
        "skills_already": [
            3,
            5
        ],
        "hobbies": [
            1,
            2
        ],
        "prog_langs": [
            1,
            3,
            5,
            6
        ]
    },

    {
        "id": 3,
        "name": "John Smith The Third",
        "email": "john@example.com",
        "ment_supp": 0.8,
        "overwhelmed": 0.4,
        "anxiety": 0.5,
        "trust": 0.6,
        "friendship": 0.2,
        "help": 0.1,
        "advice": 0.7,
        "sleep": 1.0,
        "exercise": 0.6,
        "comp_exp": 0.7,
        "field_exp": 0.6,
        "intro_extro": 1.0,
        "soft_hard_learn": 0.8,
        "soft_hard_already": 0.3,
        "skills_to_learn": [
            2,
            4
        ],
        "skills_already": [
            3,
            5
        ],
        "hobbies": [
            1,
            2
        ],
        "prog_langs": [
            1,
            3,
            5,
            6
        ]
    }
]
proglangs = [
    {
        "id": 1,
        "num_users_with_lang": 1,
        "num_projects_with_lang": 1,
        "name": "Python",
        "number": 1
    },
    {
        "id": 2,
        "num_users_with_lang": 0,
        "num_projects_with_lang": 0,
        "name": "cpp",
        "number": 2
    },
    {
        "id": 3,
        "num_users_with_lang": 1,
        "num_projects_with_lang": 0,
        "name": "Java",
        "number": 5
    },
    {
        "id": 4,
        "num_users_with_lang": 0,
        "num_projects_with_lang": 0,
        "name": "Kotlin",
        "number": 4
    },
    {
        "id": 5,
        "num_users_with_lang": 1,
        "num_projects_with_lang": 0,
        "name": "Haskell",
        "number": 6
    },
    {
        "id": 6,
        "num_users_with_lang": 1,
        "num_projects_with_lang": 0,
        "name": "Clojure",
        "number": 7
    }
]

hobbies = [
    {
        "id": 1,
        "num_users_with_hobby": 1,
        "name": "Reading",
        "number": 1
    },
    {
        "id": 2,
        "num_users_with_hobby": 1,
        "name": "Gaming",
        "number": 2
    },
    {
        "id": 3,
        "num_users_with_hobby": 0,
        "name": "Cooking",
        "number": 3
    },
    {
        "id": 4,
        "num_users_with_hobby": 0,
        "name": "Outdoor sports",
        "number": 4
    },
    {
        "id": 5,
        "num_users_with_hobby": 0,
        "name": "Indoor sports",
        "number": 5
    }
]

skills = [
    {
        "id": 2,
        "num_users_with_skill": 0,
        "num_users_want_to_learn": 1,
        "num_projects_that_need": 1,
        "num_projects_that_have": 0,
        "name": "Communication",
        "number": 2
    },
    {
        "id": 3,
        "num_users_with_skill": 1,
        "num_users_want_to_learn": 0,
        "num_projects_that_need": 1,
        "num_projects_that_have": 0,
        "name": "Programming",
        "number": 3
    },
    {
        "id": 4,
        "num_users_with_skill": 0,
        "num_users_want_to_learn": 1,
        "num_projects_that_need": 0,
        "num_projects_that_have": 1,
        "name": "Leadership",
        "number": 4
    },
    {
        "id": 5,
        "num_users_with_skill": 1,
        "num_users_want_to_learn": 0,
        "num_projects_that_need": 0,
        "num_projects_that_have": 1,
        "name": "Research",
        "number": 5
    }
]



"""""
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
"""""

# defining weight factors
std_factors = {
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
    'prog_langs': 1,
    'intro_extro': -1,
    'soft_hard_learn': 1,
    'skills_to_learn': 1,
    'soft_hard_already': 1,
    'skills_already': 1,
    'skills_project_general': 1,
    'skills_project_needed': 1,
}
hobbies_factors = {
    'ment_supp': 0,
    'overwhelmed': 0,
    'anxiety': 0,
    'trust': 0,
    'friendship': 0,
    'help': 0,
    'advice': 0,
    'sleep': 0,
    'exercise': 0,
    'hobbies': 1,
    'comp_exp': 0,
    'field_exp': 0,
    'prog_langs': 0,
    'intro_extro': 0,
    'soft_hard_learn': 0,
    'skills_to_learn': 0,
    'soft_hard_already': 0,
    'skills_already': 0,
    'skills_project_general': 0,
    'skills_project_needed': 0,
}
lang_factors = {
    'ment_supp': 0,
    'overwhelmed': 0,
    'anxiety': 0,
    'trust': 0,
    'friendship': 0,
    'help': 0,
    'advice': 0,
    'sleep': 0,
    'exercise': 0,
    'hobbies': 0,
    'comp_exp': 0,
    'field_exp': 0,
    'prog_langs': 1,
    'intro_extro': 0,
    'soft_hard_learn': 0,
    'skills_to_learn': 0,
    'soft_hard_already': 0,
    'skills_already': 0,
    'skills_project_general': 0,
    'skills_project_needed': 0,
}

critical = ['hobbies','prog_langs','skills_to_learn','skills_already','skills_project_general','skills_project_needed', 'soft_hard_learn','soft_hard_already']



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
            mat1[i,j] = mat1[j,i] = 1./(2**(min((j-i), dim - (j-i))))
    mat2 = np.identity(dim)
    count = 0
    for x in hobby_dict:
        if x['num_users_with_hobby'] == 0:
            mat2[count,count] = 1
        else:
            mat2[count,count] = 1. / np.sqrt(x['num_users_with_hobby'])
        count += 1
    mat = np.matmul(mat1,mat2)
    return mat




def get_user_by_id(user_dict, id):
    for x in user_dict:
        if x['id'] == id:
            return x
    return None


def get_user_by_name(user_dict, name):
    for x in user_dict:
        if x['name'] == name:
            return x
    return None




vec_factors = np.array([])

# Generating a vector from the factors given by the factors dictionary
def gen_vec(user,dim,factors):
    vec_factors = np.array([])
    for feat in user:
        # if feat == 'hobbies' or feat == 'programming_lan' or feat == 'skills_learn' or feat == 'skills_already':
        if feat == 'id' or feat == 'name' or feat == 'email':
            continue
        elif feat in factors:
            vec_factors = np.append(vec_factors, factors[feat])
        else:
            vec_factors = np.append(vec_factors,1)

    return vec_factors


# def gen_matrix():
#     factor_matrix = np.diag(vec_factors)


# generating a numpy vector depending on the elements from the dictionary
def gen_user_vec(user_dict):
    user = np.array([])
    for feat in user_dict:
        if feat == 'id' or feat == 'name' or feat == 'email':
            continue
        elif feat in critical:
            user = np.append(user,0) # append 0 for the critical list objects within the dictionary
        else:
            user = np.append(user,user_dict[feat])

    return user

def gen_vec_from_array(array, dim,dictionary):
    x = np.array([])
    list_of_ids = np.array([])
    for i in dictionary:
        list_of_ids = np.append(list_of_ids, i['id'])
    for i in list_of_ids:
        if i in array:
            x = np.append(x,1)
        else:
            x = np.append(x,0)
    # print(x)
    return x


# generating the matching factor contributions for the critical objects
def critical_factors(user1, user2,factors):
    dim_skills = len(skills)
    dim_hobbies = len(hobbies)
    dim_langs = len(proglangs)

    user1_hobbies = gen_vec_from_array(np.array(user1['hobbies']),dim_hobbies,hobbies)
    user2_hobbies = gen_vec_from_array(np.array(user2['hobbies']),dim_hobbies,hobbies)
    user1_skills_learn = gen_vec_from_array(np.array(user1['skills_to_learn']),dim_skills,skills)
    user1_skills_already = gen_vec_from_array(np.array(user1['skills_already']),dim_skills,skills)
    user2_skills_learn = gen_vec_from_array(np.array(user2['skills_to_learn']),dim_skills,skills)
    user2_skills_already = gen_vec_from_array(np.array(user2['skills_already']),dim_skills,skills)

    user1_prog_langs = gen_vec_from_array(np.array(user1['prog_langs']),dim_langs,proglangs)
    user2_prog_langs = gen_vec_from_array(np.array(user2['prog_langs']),dim_langs,proglangs)


    skill_mat = skill_matrix(skills)

    hobby_contribution = np.matmul(np.matmul(user1_hobbies.T, hobby_matrix(hobbies)),user2_hobbies)
    skills_contribution = (np.matmul(np.matmul(user1_skills_learn.T, skill_mat), user2_skills_already) * factors['skills_to_learn'] + np.matmul(np.matmul(user2_skills_learn.T, skill_mat), user1_skills_already)* factors['skills_already']) / 2.
    soft_hard_contribution = (abs(user1['soft_hard_learn'] - user2['soft_hard_already']) * factors['soft_hard_learn'] + abs(user2['soft_hard_learn']  - user1['soft_hard_already']) * factors['soft_hard_already']) / 2.
    prog_langs_contribution = np.matmul(user1_prog_langs.T, user2_prog_langs) * factors['prog_langs']
    # project_contribution = ( np.array(user1['skills_already']).T * np.array(user2['skills_project_needed']) + np.array(user2['skills_already']).T * np.array(user1['skills_project_needed']) ) / 2.

    # return skills_contribution + hobby_contribution + soft_hard_contribution + prog_langs_contribution + project_contribution
    return skills_contribution + hobby_contribution * factors['hobbies'] + soft_hard_contribution + prog_langs_contribution

    

# Generating the matching factor for each user combination
def matching_factor(id1,id2,factors):
    user1 = gen_user_vec(get_user_by_id(users,id1))
    user2 = gen_user_vec(get_user_by_id(users,id2))
    # factor = np.matmul(np.matmul(user1, np.diag(list(factors.values()))),user2) / (norm(user1) * norm(user2))
    factor = np.matmul(np.matmul(user1, np.diag(gen_vec(get_user_by_id(users,id1),len(user1),factors))),user2) / (norm(user1) * norm(user2)) 
    # factor = np.matmul(np.matmul(user1, np.identity(len(user1))),user2) / (norm(user1) * norm(user2))
    factor += critical_factors(get_user_by_id(users,id1), get_user_by_id(users,id2),factors)
    return factor


# Adding a new user to an existing matrix
def new_user(id,factors):
    existing_matrix = np.genfromtxt('mat.csv', delimiter=',')
    n = len(existing_matrix[0,:])
    list_of_ids = np.array([])
    for i in users:
        if id != i['id']:
            list_of_ids = np.append(list_of_ids, i['id'])
    new_matrix = np.hstack((existing_matrix, np.atleast_2d(np.zeros(n)).T))   
    new_matrix = np.vstack((new_matrix, np.atleast_2d(np.zeros(n+1))))

    for i in range(0,n):
        coefficient = matching_factor(list_of_ids[i],id,factors)
        new_matrix[i,n] = coefficient
        new_matrix[n,i] = coefficient
    new_matrix[n,n] = matching_factor(id,id,factors)

    np.savetxt("mat.csv",new_matrix, delimiter=',')  

def init_mat(factors):
    n = len(users)
    list_of_ids = np.array([])
    for i in users:
        list_of_ids = np.append(list_of_ids, i['id'])
    mat = np.zeros((n,n))
    for i in range(0,n):
        # for j in range(i + 1,n):
        for j in range(i,n):
            coeff = matching_factor(list_of_ids[i],list_of_ids[j],factors)
            mat[i,j] = mat[j,i] = coeff
    np.savetxt("mat.csv",mat,delimiter=',')



#__________DEFINE THE USED FACTORS FOR THE ALGORITHM + RUN___________

factors = {
    'std': std_factors,
    'hobbies': hobbies_factors,
    'prog_lang': lang_factors,
}

init_mat(factors['prog_lang'])
# new_user(3.)

