CREATE DATABASE CodeDuel;

USE CodeDuel;

CREATE TABLE Directory (
    d_id VARCHAR(20) NOT NULL,
    d_path VARCHAR(100) NOT NULL
);

CREATE TABLE Contestant (
    c_id INTEGER PRIMARY KEY,
    password VARCHAR(20) NOT NULL,
    reg_id VARCHAR(20) NOT NULL,
    c_name VARCHAR(50) NOT NULL,
    c_college VARCHAR(10) NOT NULL,
    c_year INTEGER NOT NULL
);

CREATE TABLE Problem (
    p_id INTEGER PRIMARY KEY,
    c_id INTEGER NOT NULL,
    p_title VARCHAR(20) NOT NULL,
    p_rating INTEGER
);

ALTER TABLE Problem
ADD CONSTRAINT c_id_fk_problem FOREIGN KEY(c_id) REFERENCES Contestant(c_id);

CREATE TABLE Testcase (
    t_id INTEGER PRIMARY KEY,
    p_id INTEGER NOT NULL,
    t_inputfile VARCHAR(20) NOT NULL,
    t_outputfile VARCHAR(20) NOT NULL,
    t_points INTEGER NOT NULL
);

ALTER TABLE Testcase
ADD CONSTRAINT p_id_fk_testcase FOREIGN KEY(p_id) REFERENCES Problem(p_id);

CREATE TABLE Score (
    c_id INTEGER NOT NULL,
    t_id INTEGER NOT NULL,
    points INTEGER NOT NULL,
    s_timestamp TIMESTAMP NOT NULL
);

ALTER TABLE Score
ADD CONSTRAINT c_id_fk_score FOREIGN KEY(c_id) REFERENCES Contestant(c_id),
ADD CONSTRAINT t_id_fk_score FOREIGN KEY(t_id) REFERENCES Testcase(t_id);

CREATE TABLE Duel (
    duel_id INTEGER NOT NULL,
    c_id_A INTEGER NOT NULL,
    c_id_B INTEGER NOT NULL
);

ALTER TABLE Duel
ADD CONSTRAINT c_id_A_Duel FOREIGN KEY(c_id_A) REFERENCES Contestant(c_id),
ADD CONSTRAINT c_id_B_Duel FOREIGN KEY(c_id_B) REFERENCES Contestant(c_id);