import random
import string
from datetime import date
from datetime import datetime
import random
from db_queries import *
import yaml

def get_rand_day():
    start_dt = date.today().replace(day=1, month=1).toordinal()
    end_dt = date.today().toordinal()
    random_day = date.fromordinal(random.randint(start_dt, end_dt))
    return random_day

def get_rand_string(len):
    N = len
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def get_districts():
    districts = []
    num = 3
    for i in range(num):
        district = {}
        district['name'] = get_rand_string(10)
        district['id'] = i+1
        districts.append(district)
    return districts

def get_rers():
    rers = []
    num = 4
    for i in range(num):
        rer = {}
        rer['description'] = get_rand_string(10)
        rer['id'] = i+1
        rers.append(rer)
    return rers

def get_schools(districts):
    schools = []
    num = 5
    for i in range(num):
        school = {}
        school['id'] = i+1
        district = districts[random.randint(0,len(districts)-1)]
        school['district_id'] = district['id']
        school['name'] = get_rand_string(10)
        schools.append(school)
    return schools

def get_classrooms(schools):
    classrooms = []
    num = 10 
    for i in range(num):
        classroom = {}
        classroom['id'] = i+1
        school = schools[random.randint(0,len(schools)-1)]
        classroom['school_id'] = school['id']
        classroom['capacity'] = random.randint(1, 2)
        classrooms.append(classroom)
    return classrooms

def get_students(schools):
    students = []
    num = 15 
    for i in range(num):
        student = {}
        student['id'] = i+1
        student['first_name'] = get_rand_string(10) 
        student['last_name'] = get_rand_string(10) 
        school = schools[random.randint(0,len(schools)-1)]
        student['school_id'] = school['id']
        students.append(student)
    return students

def get_subjs():
    subjs = []
    num = 4
    for i in range(num):
        subj = {}
        subj['description'] = get_rand_string(40)
        subj['id'] = i+1
        subj['min_grade'] = random.randint(0, 20)
        subjs.append(subj)
    return subjs

def get_req_subjs(subjs):
    req_subjs = []
    for subj in subjs:
        if (random.randint(0, 1) == 1):
            req_subj = {}
            req_subj['subj_id'] = subj['id']
            req_subjs.append(req_subj)
    return req_subjs

def get_student_subjs(students, subjs, req_subjs): 
    student_subjs = []
    for student in students:
        for subj in subjs:
            if (random.randint(0, 3) != 1):
                student_subj = {}
                student_subj['student_id'] = student['id']
                student_subj['subj_id'] = subj['id']
                student_subjs.append(student_subj)
    return student_subjs

def get_exams(subjs):
    exams = []
    for subj in subjs:
        exam1 = {}
        exam2 = {}
        exam1['subj_id'] = subj['id']
        exam1['day'] = get_rand_day()
        exam1['id'] = len(exams) + 1  
        exams.append(exam1)
        exam2['subj_id'] = subj['id']
        exam2['day'] = get_rand_day()
        exam2['id'] = len(exams) + 1  
        exams.append(exam2)
    return exams
