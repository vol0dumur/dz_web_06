-- Знайти список курсів, які відвідує студент. Для студента з id = 25
SELECT sub.name AS subject_name
FROM student_subjects ss
JOIN subjects sub ON ss.subject_id = sub.id
WHERE ss.student_id = 25;