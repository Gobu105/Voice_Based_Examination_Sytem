DROP TABLE evaluations;
DROP TABLE answers;
DROP TABLE exam_sessions;
DROP TABLE questions;
DROP TABLE exams;
DROP TABLE candidates;
DROP TABLE login;
DROP TABLE registration;


CREATE TABLE registration (
    reg_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('INVIGILATOR','CANDIDATE') NOT NULL,
    phone_no VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE login (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    reg_id INT UNIQUE,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    last_login TIMESTAMP,
    FOREIGN KEY (reg_id) REFERENCES registration(reg_id)
);

CREATE TABLE candidates (
    candidate_id INT AUTO_INCREMENT PRIMARY KEY,
    reg_id INT UNIQUE,
    registration_no VARCHAR(50) UNIQUE,
    FOREIGN KEY (reg_id) REFERENCES registration(reg_id)
);

CREATE TABLE exams (
    exam_id INT AUTO_INCREMENT PRIMARY KEY,
    exam_name VARCHAR(100),
    duration INT,
    total_marks INT,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES registration(reg_id)
);

CREATE TABLE questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    exam_id INT,
    question_text TEXT,
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id)
);

CREATE TABLE exam_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    exam_id INT,
    candidate_id INT,
    start_time DATETIME,
    end_time DATETIME,
    status ENUM('STARTED','SUBMITTED','ENDED'),
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
);

CREATE TABLE answers (
    answer_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    question_id INT,
    answer_text TEXT,
    FOREIGN KEY (session_id) REFERENCES exam_sessions(session_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);

CREATE TABLE evaluations (
    evaluation_id INT AUTO_INCREMENT PRIMARY KEY,
    answer_id INT UNIQUE,
    marks_awarded INT,
    evaluated_by INT,
    FOREIGN KEY (answer_id) REFERENCES answers(answer_id),
    FOREIGN KEY (evaluated_by) REFERENCES registration(reg_id)
);

DESC TABLE evaluations;
DESC TABLE answers;
DESC TABLE exam_sessions;
DESC TABLE questions;
DESC TABLE exams;
DESC TABLE candidates;
DESC TABLE login;
DESC TABLE registration;

