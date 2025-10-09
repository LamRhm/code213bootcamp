-- 1. Create database
CREATE DATABASE if not exists pwelett_hackard;

-- Use the database
USE pwelett_hackard;

---------------------------------------------------------
-- 2. Create tables
---------------------------------------------------------

-- employees table
CREATE TABLE if not exists employees (
    emp_no INT PRIMARY KEY,
    birth_date DATE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender ENUM('M','F'),
    hire_date DATE
);

-- salaries table
CREATE TABLE salaries (
    emp_no INT,
    salary INT,
    from_date DATE,
    to_date DATE,
    PRIMARY KEY (emp_no, from_date),
    FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);

-- titles table
CREATE TABLE titles (
    emp_no INT,
    title VARCHAR(50),
    from_date DATE,
    to_date DATE,
    PRIMARY KEY (emp_no, from_date),
    FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);

-- departments table
CREATE TABLE departments (
    dept_no CHAR(4) PRIMARY KEY,
    dept_name VARCHAR(50) UNIQUE
);

-- dept_emp table
CREATE TABLE dept_emp (
    emp_no INT,
    dept_no CHAR(4),
    from_date DATE,
    to_date DATE,
    PRIMARY KEY (emp_no, dept_no),
    FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
    FOREIGN KEY (dept_no) REFERENCES departments(dept_no)
);

-- dept_manager table
CREATE TABLE dept_manager (
    emp_no INT,
    dept_no CHAR(4),
    from_date DATE,
    to_date DATE,
    PRIMARY KEY (emp_no, dept_no),
    FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
    FOREIGN KEY (dept_no) REFERENCES departments(dept_no)
);

---------------------------------------------------------
-- 3. Insert data
---------------------------------------------------------

-- employees
INSERT INTO employees VALUES
(10001,'1960-01-15','John','Smith','M','1985-06-01'),
(10002,'1958-07-24','Hercules','Brown','M','1986-03-12'),
(10003,'1965-09-30','Mary','Johnson','F','1987-11-05'),
(10004,'1962-03-11','David','Williams','M','1983-02-20'),
(10005,'1968-12-25','Susan','Jones','F','1989-09-17'),
(10006,'1961-06-06','Robert','White','M','1986-08-22');

-- salaries
INSERT INTO salaries VALUES
(10001,45000,'1985-06-01','1990-12-31'),
(10002,52000,'1986-03-12','1990-12-31'),
(10003,48000,'1987-11-05','1990-12-31'),
(10004,60000,'1983-02-20','1990-12-31'),
(10005,41000,'1989-09-17','1990-12-31'),
(10006,53000,'1986-08-22','1990-12-31');

-- titles
INSERT INTO titles VALUES
(10001,'Engineer','1985-06-01','1990-12-31'),
(10002,'Senior Engineer','1986-03-12','1990-12-31'),
(10003,'Staff','1987-11-05','1990-12-31'),
(10004,'Manager','1983-02-20','1990-12-31'),
(10005,'Engineer','1989-09-17','1990-12-31'),
(10006,'Engineer','1986-08-22','1990-12-31');

-- departments
INSERT INTO departments VALUES
('d001','Sales'),
('d002','Development'),
('d003','Finance'),
('d004','HR');

-- dept_emp
INSERT INTO dept_emp VALUES
(10001,'d002','1985-06-01','1990-12-31'),
(10002,'d001','1986-03-12','1990-12-31'),
(10003,'d001','1987-11-05','1990-12-31'),
(10004,'d003','1983-02-20','1990-12-31'),
(10005,'d002','1989-09-17','1990-12-31'),
(10006,'d001','1986-08-22','1990-12-31');

-- dept_manager
INSERT INTO dept_manager VALUES
(10004,'d003','1983-02-20','1990-12-31'), -- Finance
(10002,'d001','1988-01-01','1990-12-31'), -- Sales
(10001,'d002','1987-05-01','1990-12-31'), -- Development
(10006,'d004','1989-01-01','1990-12-31'); -- HR
