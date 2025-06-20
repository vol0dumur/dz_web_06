-- Список курсів, які певному студенту читає певний викладач. Для студента з id = 40 і викладача з id = 3. Може бути пустий результат.
SELECT sub.name AS subject_name
FROM student_subjects ss
JOIN subjects sub ON ss.subject_id = sub.id
WHERE ss.student_id = 40 AND sub.teacher_id = 3;