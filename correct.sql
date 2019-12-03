3:
select * from
student_subj
left join
(select distinct student_subj.student_id, subj_id from
(select student_id,exam_id
from student_distrib,exam_distrib
where exam_distrib_id = exam_distrib.id) as t1, student_subj
where
student_subj.student_id = t1.student_id
order by student_subj.student_id, subj_id) as t2
on
t2.student_id = student_subj.student_id
and t2.subj_id = student_subj.subj_id;

4:
select id as student_id, req_subj.subj_id as rsi
from student,req_subj

except

select student_subj.student_id, req_subj.subj_id as rsi
from
req_subj,student_subj
where req_subj.subj_id = student_subj.subj_id 
order by rsi;

5:
not in his school:

select id from
student

except

select t2.student_id from
classroom,
(select student_id, school_id, t1.classroom_id
from
student,
(select student_id, classroom_id
from student_distrib,exam_distrib
where exam_distrib_id = exam_distrib.id) as t1
where student.id = t1.student_id) as t2
where classroom.id = t2.classroom_id
	  and classroom.school_id = t2.school_id;



1st exams t00:
select exam.id as exam_id, exam.subj_id, exam.day
from exam,
(select subj_id, min(day) as day
from exam
group by subj_id order by subj_id) as t1
where exam.day = t1.day;

reserved_exams t0:
select exam.id, exam.subj_id, exam.day
from exam,
(select subj_id, max(day) as day
from exam
group by subj_id order by subj_id) as t1
where exam.day = t1.day;


student->exam_id t1:
select student_distrib.student_id, exam_distrib.exam_id
from
student_distrib, exam_distrib
where student_distrib.exam_distrib_id=exam_distrib.id;


student->exam_id->subj_id t2:
select t1.student_id, t1.exam_id, exam.subj_id
from
exam,
(select student_distrib.student_id, exam_distrib.exam_id
from
student_distrib, exam_distrib
where student_distrib.exam_distrib_id=exam_distrib.id) as t1
where
exam.id = t1.exam_id;

student on reserved exam t3:
select t2.student_id, t2.exam_id, t2.subj_id from
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
t0.id = t2.exam_id;

student on reserved exam with reason t4:
select t3.student_id, t3.subj_id, student_rer.rer_id
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
   t3.subj_id=student_rer.subj_id;

student with no rsr on rsrv exam t5: 
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
where t4.rer_id is NULL; 

student grades t6:
select grade.student_id, exam.subj_id, grade.grade, exam.id as exam_id
from
grade, exam
where
grade.exam_id = exam.id;

student grades for the 1st exam t7:
select t6.student_id, t6.subj_id, t6.grade
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
t6.exam_id = t00.exam_id;

student with small grades t8:
select t7.student_id, t7.subj_id, t7.grade, subj.min_grade
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
where t7.subj_id = subj.id and subj.min_grade > t7.grade;


student not allowed to be rsrv exam t9:

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
