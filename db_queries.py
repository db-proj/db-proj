import psycopg2
import os

con = psycopg2.connect(database="postgres", password="", host="127.0.0.1",
                       port="5432")

def tables_create():
    os.system("psql -f exam.sql -d postgres")
#  def tables_delete():
    #  os.system("psql -f del_exam.sql -d postgres")

def district_add_raw(name):
    cur = con.cursor()
    cur.execute(f'''
    insert into district (name)
    values ('{name}');
    ''')
    con.commit()

def school_add_raw(district_id, name):
    cur = con.cursor()
    cur.execute(f'''
    insert into school (district_id, name)
    values ('{district_id}', '{name}');
    ''')
    con.commit()

def classroom_add_raw(school_id, capacity):
    cur = con.cursor()
    cur.execute(f'''
    insert into classroom (school_id, capacity)
    values ('{school_id}', '{capacity}');
    ''')
    con.commit()

def student_add_raw(first_name, last_name, school_id):
    cur = con.cursor()
    cur.execute(f'''
    insert into student (first_name, last_name, school_id)
    values ('{first_name}', '{last_name}', '{school_id}');
    ''')
    con.commit()

def subj_add_raw(description, min_grade):
    cur = con.cursor()
    cur.execute(f'''
    insert into subj (description, min_grade)
    values ('{description}', '{min_grade}');
    ''')
    con.commit()

def student_subj_add_raw(student_id, subj_id):
    cur = con.cursor()
    cur.execute(f'''
    insert into student_subj (student_id, subj_id)
    values ('{student_id}', '{subj_id}');
    ''')
    con.commit()

def req_subj_add_raw(subj_id):
    cur = con.cursor()
    cur.execute(f'''
    insert into req_subj (subj_id)
    values ('{subj_id}');
    ''')
    con.commit()

def exam_add_raw(subj_id, day):
    cur = con.cursor()
    cur.execute(f'''
    insert into exam (subj_id, day)
    values ('{subj_id}', '{day}');
    ''')
    con.commit()

def grade_add_raw(student_id, exam_id, grade):
    cur = con.cursor()
    cur.execute(f'''
    insert into grade (student_id, exam_id, grade)
    values ('{student_id}', '{exam_id}', '{grade}');
    ''')
    con.commit()

def rer_add_raw(description):
    cur = con.cursor()
    cur.execute(f'''
    insert into rer (description)
    values ('{description}');
    ''')
    con.commit()

def student_rer_add_raw(student_id, rer_id, subj_id):
    cur = con.cursor()
    cur.execute(f'''
    insert into student_rer (student_id, rer_id, subj_id)
    values ('{student_id}', '{rer_id}', '{subj_id}');
    ''')
    con.commit()

def exam_distrib_add_raw(classroom_id, exam_id):
    cur = con.cursor()
    cur.execute(f'''
    insert into exam_distrib (classroom_id, exam_id)
    values ('{classroom_id}', '{exam_id}');
    ''')
    con.commit()

def student_distrib_add_raw(student_id, exam_distrib_id):
    cur = con.cursor()
    cur.execute(f'''
    insert into student_distrib (student_id, exam_distrib_id)
    values ('{student_id}', '{exam_distrib_id}');
    ''')
    con.commit()
