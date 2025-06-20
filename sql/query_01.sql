-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT s.full_name, ROUND(AVG(g.grade), 2) AS avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 5;