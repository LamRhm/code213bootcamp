SELECT d.dept_no, d.dept_name,
       e.emp_no, e.last_name, e.first_name,
       dm.from_date, dm.to_date
FROM departments d
JOIN dept_manager dm ON d.dept_no = dm.dept_no
JOIN employees e ON dm.emp_no = e.emp_no;
