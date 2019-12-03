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

def students_not_allowed_for_rsrv():
    cur = con.cursor()
    cur.execute(f'''
select t4.student_id, t4.subj_id from
(select t3.student_id, t3.subj_id, student_rer.rer_id
from
(select t2.student_id, t2.exam_id, t2.subj_id from
(select t1.student_id, t1.exam_id, exam.subj_id
from
exam,
(select student_distrib.student_id, exam_distrib.exam_id
from
student_distrib, exam_distrib
where student_distrib.exam_distrib_id=exam_distrib.id) as t1
where
exam.id = t1.exam_id) as t2,
(select exam.id, exam.subj_id, exam.day
from exam,
(select subj_id, max(day) as day
from exam
group by subj_id order by subj_id) as t1
where exam.day = t1.day) as t0
where
t0.id = t2.exam_id) as t3
left join student_rer
on t3.student_id=student_rer.student_id and
   t3.subj_id=student_rer.subj_id) as t4
where t4.rer_id is NULL

except

(
select t4.student_id, t4.subj_id from
(select t3.student_id, t3.subj_id, student_rer.rer_id
from
(select t2.student_id, t2.exam_id, t2.subj_id from
(select t1.student_id, t1.exam_id, exam.subj_id
from
exam,
(select student_distrib.student_id, exam_distrib.exam_id
from
student_distrib, exam_distrib
where student_distrib.exam_distrib_id=exam_distrib.id) as t1
where
exam.id = t1.exam_id) as t2,
(select exam.id, exam.subj_id, exam.day
from exam,
(select subj_id, max(day) as day
from exam
group by subj_id order by subj_id) as t1
where exam.day = t1.day) as t0
where
t0.id = t2.exam_id) as t3
left join student_rer
on t3.student_id=student_rer.student_id and
   t3.subj_id=student_rer.subj_id) as t4
where t4.rer_id is NULL

intersect

select t7.student_id, t7.subj_id
from
subj,
(select t6.student_id, t6.subj_id, t6.grade
from
(select grade.student_id, exam.subj_id, grade.grade, exam.id as exam_id
from
grade, exam
where
grade.exam_id = exam.id) as t6,
(select exam.id as exam_id, exam.subj_id, exam.day
from exam,
(select subj_id, min(day) as day
from exam
group by subj_id order by subj_id) as t1
where exam.day = t1.day) as t00
where
t6.exam_id = t00.exam_id) as t7
where t7.subj_id = subj.id and subj.min_grade > t7.grade
);
    ''')
    rows = cur.fetchall()
    print("Students not allowed for rsrv exam:")
    print("(student_id, subj_id)")
    for row in rows:
        print(row)
    con.commit()

def students_with_rer_not_assigned_rsrv():
    cur = con.cursor()
    cur.execute(f'''
select r0.student_id,r0.subj_id,r0.exam_id from
(select student_rer.student_id,student_rer.subj_id,t0.id as exam_id from
student_rer,
(select exam.id, exam.subj_id, exam.day
from exam,
(select subj_id, max(day) as day
from exam
group by subj_id order by subj_id) as t1
where exam.day = t1.day) as t0
where student_rer.subj_id=t0.subj_id)
as r0
left join
(select t2.student_id, t2.exam_id, t2.subj_id from
(select t1.student_id, t1.exam_id, exam.subj_id
from
exam,
(select student_distrib.student_id, exam_distrib.exam_id
from
student_distrib, exam_distrib
where student_distrib.exam_distrib_id=exam_distrib.id) as t1
where
exam.id = t1.exam_id) as t2,
(select exam.id, exam.subj_id, exam.day
from exam,
(select subj_id, max(day) as day
from exam
group by subj_id order by subj_id) as t1
where exam.day = t1.day) as t0
where
t0.id = t2.exam_id)
as t3
on r0.student_id=t3.student_id and r0.subj_id=t3.subj_id
where t3.student_id is NULL;

    ''')
    rows = cur.fetchall()
    print("Students with rer not assigned to rsrv exam") 
    print("(student_id, subj_id)")
    for row in rows:
        print(row[0], row[1])
    con.commit()

def students_with_low_grades_not_assigned_rsrv():
    cur = con.cursor()
    cur.execute(f'''
select t8.student_id,t8.subj_id,t8.grade,t8.min_grade,t3.exam_id 
from
(select t7.student_id, t7.subj_id, t7.grade, subj.min_grade
from
subj,
(select t6.student_id, t6.subj_id, t6.grade
from
(select grade.student_id, exam.subj_id, grade.grade, exam.id as exam_id
from
grade, exam
where
grade.exam_id = exam.id) as t6,
(select exam.id as exam_id, exam.subj_id, exam.day
from exam,
(select subj_id, min(day) as day
from exam
group by subj_id order by subj_id) as t1
where exam.day = t1.day) as t00
where
t6.exam_id = t00.exam_id) as t7
where t7.subj_id = subj.id and subj.min_grade > t7.grade)
as t8
left join
(select t2.student_id, t2.exam_id, t2.subj_id from
(select t1.student_id, t1.exam_id, exam.subj_id
from
exam,
(select student_distrib.student_id, exam_distrib.exam_id
from
student_distrib, exam_distrib
where student_distrib.exam_distrib_id=exam_distrib.id) as t1
where
exam.id = t1.exam_id) as t2,
(select exam.id, exam.subj_id, exam.day
from exam,
(select subj_id, max(day) as day
from exam
group by subj_id order by subj_id) as t1
where exam.day = t1.day) as t0
where
t0.id = t2.exam_id)
as t3
on t8.student_id=t3.student_id and t8.subj_id=t3.subj_id
where t3.exam_id is NULL;
    ''')
    rows = cur.fetchall()
    print("Students with low grades not assigned for rsrv exam:")
    print("(student_id, subj_id, grade, min_grade)")
    for row in rows:
        print(row[0], row[1], row[2], row[3])
    con.commit()

def not_assigned_to_1st_exam_of_selected_subj():
    cur = con.cursor()
    cur.execute(f'''
select student_subj.student_id,student_subj.subj_id from
student_subj
left join
(select t1.student_id, t1.exam_id, exam.subj_id
from
exam,
(select student_distrib.student_id, exam_distrib.exam_id
from
student_distrib, exam_distrib
where student_distrib.exam_distrib_id=exam_distrib.id) as t1
where
exam.id = t1.exam_id)
as t2
on t2.subj_id = student_subj.subj_id and
   t2.student_id = student_subj.student_id
where
	t2.exam_id is NULL
order by student_subj.student_id;
    ''')
    rows = cur.fetchall()
    print("not_assigned_to_1st_exam_of_selected_subj")
    print("(student_id, subj_id)")
    for row in rows:
        print(row)
    con.commit()
