-- Для групи з id = 1 і предмета з id = 2
SELECT s.full_name, g.grade, g.grade_date
FROM grades g
JOIN students s ON g.student_id = s.id
WHERE s.group_id = 1 AND g.subject_id = 2
ORDER BY g.grade_date;