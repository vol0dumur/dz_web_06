-- Для предмету з id = 5
SELECT gr.name AS group_name, ROUND(AVG(g.grade), 2) AS avg_grade
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN groups gr ON s.group_id = gr.id
WHERE g.subject_id = 5
GROUP BY gr.id
ORDER BY avg_grade DESC;