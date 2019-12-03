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


students with rer and their second exam id r0:
select student_rer.student_id,student_rer.subj_id,t0.id as exam_id from
student_rer,
(select exam.id, exam.subj_id, exam.day
from exam,
(select subj_id, max(day) as day
from exam
group by subj_id order by subj_id) as t1
where exam.day = t1.day) as t0
where student_rer.subj_id=t0.subj_id;


student with rer but no assigned to any second exam r1:
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


students with small grades no assigned to second exam r2:
/*
 * select t8.student_id,t8.subj_id,t8.grade,t8.min_grade
 */
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


student not assigned to 1st exam for some of chosen subj r3;
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


students with num of choseh req subj r4: 
select student_subj.student_id,count(student_subj.subj_id) from
student_subj,req_subj
where student_subj.subj_id = req_subj.subj_id
group by student_id
order by student_id;

students with not all req subjs choosen r5:
select r4.student_id from
(select student_subj.student_id,count(student_subj.subj_id) from
student_subj,req_subj
where student_subj.subj_id = req_subj.subj_id
group by student_id
order by student_id)
as r4
where r4.count <> (select count(*) from req_subj);



student->exam_id->classroom_id r6:
select student_distrib.student_id, exam_distrib.exam_id,
	   exam_distrib.classroom_id
from
student_distrib, exam_distrib
where student_distrib.exam_distrib_id=exam_distrib.id;

student->district r7:
select student.id,school.district_id 
from student,school where
student.school_id = school.id;

classroom->district r8:
select classroom.id,school.district_id 
from classroom,school where
classroom.school_id = school.id;

students in classrooms of not theirs districts r9:
select r6.student_id,r6.classroom_id,r7.district_id as sdi,
	   r8.district_id as cdi,r6.exam_id
from
(select student_distrib.student_id, exam_distrib.exam_id,
	   exam_distrib.classroom_id
from
student_distrib, exam_distrib
where student_distrib.exam_distrib_id=exam_distrib.id)
as r6,
(select student.id,school.district_id 
from student,school where
student.school_id = school.id)
as r7,
(select classroom.id,school.district_id 
from classroom,school where
classroom.school_id = school.id)
as r8
where r6.student_id=r7.id and
	  r6.classroom_id=r8.id and 
	  r7.district_id <> r8.district_id;


students in classrooms of their school r10:
select student.id as student_id, classroom.id as classroom_id,
	   student.school_id as ssi,
	   classroom.school_id as csi,
	   r6.exam_id
from
(select student_distrib.student_id, exam_distrib.exam_id,
	   exam_distrib.classroom_id
from
student_distrib, exam_distrib
where student_distrib.exam_distrib_id=exam_distrib.id)
as r6,student,classroom
where
r6.student_id=student.id and classroom.id=r6.classroom_id
and student.school_id=classroom.school_id;



s1:
select exam_id,classroom_id,count(student_id) as cnt from
student_distrib,exam_distrib where
student_distrib.exam_distrib_id = exam_distrib.id
group by exam_id, classroom_id;

count is more than capacity s2:
select s1.classroom_id, s1.exam_id, s1.cnt, classroom.capacity
from
(select exam_id,classroom_id,count(student_id) as cnt from
student_distrib,exam_distrib where
student_distrib.exam_distrib_id = exam_distrib.id
group by exam_id, classroom_id)
as s1,
classroom
where s1.classroom_id = classroom.id and
	  s1.cnt > classroom.capacity;
