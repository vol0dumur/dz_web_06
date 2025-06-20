-- Знайти середній бал, який ставить певний викладач зі своїх предметів. Для викладача з id = 3
SELECT t.full_name, ROUND(AVG(g.grade), 2) AS avg_grade
FROM grades g
JOIN subjects sub ON g.subject_id = sub.id
JOIN teachers t ON sub.teacher_id = t.id
WHERE t.id = 3
GROUP BY t.id;