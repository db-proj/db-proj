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

def fill_data(from_conf):
    if from_conf:
        with open('conf/districts') as f:
            districts = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/schools') as f:
            schools = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/classrooms') as f:
            classrooms = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/students') as f:
            students = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/subjs') as f:
            subjs = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/req_subjs') as f:
            req_subjs = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/exams') as f:
            exams = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/student_subjs') as f:
            student_subjs = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/grades') as f:
            grades = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/exam_distribs') as f:
            exam_distribs = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/student_distribs') as f:
            student_distribs = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/rers') as f:
            rers = yaml.load(f, Loader=yaml.FullLoader)
        with open('conf/student_rers') as f:
            student_rers = yaml.load(f, Loader=yaml.FullLoader)
    else:
        districts = get_districts()
        schools = get_schools(districts)
        classrooms = get_classrooms(schools)
        students = get_students(schools)
        subjs = get_subjs()
        req_subjs = get_req_subjs(subjs)
        student_subjs = get_student_subjs(students, subjs, req_subjs)
        exams = get_exams(subjs)
        rers = get_rers()

        exam_distribs = []
        for classroom in classrooms:
            for exam in exams:
                exam_distrib = {}
                exam_distrib['id'] = len(exam_distribs) + 1
                exam_distrib['classroom_id'] = classroom['id']
                exam_distrib['exam_id'] = exam['id']
                exam_distribs.append(exam_distrib)

        student_distribs = []
        grades = []
        student_rers = []
        for student in students:
            this_student_subjs = []
            for i in student_subjs:
                if (i['student_id'] == student['id']):
                    this_student_subjs.append(i['subj_id'])

            for subj_id in this_student_subjs:
                #skip some
                if (random.randint(0, 3) == 1):
                    break

                subj_exam1 = {}
                subj_exam2 = {}
                for exam in exams:
                    if (exam['subj_id'] == subj_id):
                        if (bool(subj_exam1)):
                            subj_exam2 = exam
                        else:
                            subj_exam1 = exam

                if (subj_exam1['day'] > subj_exam2['day']):
                    subj_exam1, subj_exam2 = subj_exam2, subj_exam1

                exam_distrib = {}
                student_distrib1 = {}
                student_distrib2 = {}
                need_second_exam = False
                for i in exam_distribs:
                    if (i['exam_id'] == subj_exam1['id'] and \
                        random.randint(0, 5) == 1):

                        student_distrib1['student_id'] = student['id']
                        student_distrib1['exam_distrib_id'] = i['id']

                        if (random.randint(0, 4) != 1):
                            grade = {}
                            grade['student_id'] = student['id']
                            grade['exam_id'] = subj_exam1['id']
                            grade['grade'] = random.randint(0, 100)
                            grades.append(grade)
                            if (grade['grade'] < 30):
                                need_second_exam = True
                        else:
                            need_second_exam = True
                            student_rer = {}
                            for rer in rers:
                                if (random.randint(0, 1) == 1):
                                    student_rer = {}
                                    student_rer['student_id'] = student['id']
                                    student_rer['subj_id'] = subj_id
                                    student_rer['rer_id'] = rer['id']
                                    student_rers.append(student_rer)
                                    break

                        student_distribs.append(student_distrib1)
                        break

                for i in exam_distribs:
                    if (not need_second_exam):
                        break
                    if (i['exam_id'] == subj_exam2['id'] and \
                        random.randint(0, 6) == 1):

                        student_distrib2['student_id'] = student['id']
                        student_distrib2['exam_distrib_id'] = i['id']
                        if (random.randint(0, 4) != 1):
                            grade = {}
                            grade['student_id'] = student['id']
                            grade['exam_id'] = subj_exam2['id']
                            grade['grade'] = random.randint(0, 100)
                            grades.append(grade)
                        student_distribs.append(student_distrib2)
                        break


    for district in districts:
        district_add_raw(district['name'])

    for school in schools:
        school_add_raw(school['district_id'], school['name'])

    for classroom in classrooms:
        classroom_add_raw(classroom['school_id'], classroom['capacity'])

    for student in students:
        student_add_raw(student['first_name'],
                        student['last_name'],
                        student['school_id'])

    for subj in subjs:
        subj_add_raw(subj['description'], subj['min_grade'])

    for req_subj in req_subjs:
        req_subj_add_raw(req_subj['subj_id'])

    for exam in exams:
        exam_add_raw(exam['subj_id'], exam['day'])

    for student_subj in student_subjs:
        student_subj_add_raw(student_subj['student_id'],
                             student_subj['subj_id'])

    for grade in grades:
        grade_add_raw(grade['student_id'], grade['exam_id'],
                      grade['grade'])

    for exam_distrib in exam_distribs:
        exam_distrib_add_raw(exam_distrib['classroom_id'],
                             exam_distrib['exam_id'])

    for student_distrib in student_distribs:
        student_distrib_add_raw(student_distrib['student_id'],
                                student_distrib['exam_distrib_id'])

    for rer in rers:
        rer_add_raw(rer['description'])

    for student_rer in student_rers:
        student_rer_add_raw(student_rer['student_id'],
                            student_rer['rer_id'],
                            student_rer['subj_id'])

    with open('conf/districts', 'w') as f:
        yaml.dump(districts, f)
    with open('conf/schools', 'w') as f:
        yaml.dump(schools, f)
    with open('conf/classrooms', 'w') as f:
        yaml.dump(classrooms, f)
    with open('conf/students', 'w') as f:
        yaml.dump(students, f)
    with open('conf/subjs', 'w') as f:
        yaml.dump(subjs, f)
    with open('conf/req_subjs', 'w') as f:
        yaml.dump(req_subjs, f)
    with open('conf/exams', 'w') as f:
        yaml.dump(exams, f)
    with open('conf/student_subjs', 'w') as f:
        yaml.dump(student_subjs, f)
    with open('conf/grades', 'w') as f:
        yaml.dump(grades, f)
    with open('conf/exam_distribs', 'w') as f:
        yaml.dump(exam_distribs, f)
    with open('conf/student_distribs', 'w') as f:
        yaml.dump(student_distribs, f)
    with open('conf/rers', 'w') as f:
        yaml.dump(rers, f)
    with open('conf/student_rers', 'w') as f:
        yaml.dump(student_rers, f)

if __name__ == "__main__":
    #  fill_data(from_conf = False)
    fill_data(from_conf = True)
    students_not_allowed_for_rsrv()
    students_with_rer_not_assigned_rsrv()
