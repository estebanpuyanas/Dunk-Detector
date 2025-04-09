DROP DATABASE IF EXISTS dunkDetector;
CREATE DATABASE IF NOT EXISTS dunkDetector;

USE dunkDetector;

-- User table:
CREATE TABLE users
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    firstName  varchar(50) NOT NULL,
    middleName varchar(50),
    lastName varchar(50) NOT NULL,
    mobile varchar(15),
    email varchar(75) UNIQUE NOT NULL,
    role enum ('admin', 'agent', 'player', 'system administrator', 'data analyst', 'general manager', 'coach') NOT NULL, # Adjust as needed

    INDEX (mobile),
    INDEX (email),
    INDEX (id)
);

-- Agent table:
CREATE TABLE agents
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    firstName varchar(50) NOT NULL,
    middleName varchar(50),
    lastName varchar(50) NOT NULL,
    mobile varchar(15),
    email varchar(75) UNIQUE NOT NULL,

    INDEX (mobile),
    INDEX (email),
    INDEX (id)
);

-- Coach table:
CREATE TABLE coaches
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    firstName  varchar(50) NOT NULL,
    middleName varchar(50),
    lastName   varchar(50) NOT NULL,
    mobile varchar(15),
    email varchar(75) UNIQUE NOT NULL,
    teamId integer NOT NULL,
    agentId integer NOT NULL,

    FOREIGN KEY (agentId) REFERENCES agents (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (mobile),
    INDEX (email),
    INDEX (id),
    INDEX (teamId)
);

-- General Manager table:
CREATE TABLE general_managers
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    firstName  varchar(50) NOT NULL,
    middleName varchar(50),
    lastName varchar(50) NOT NULL,
    mobile varchar(15),
    email varchar(75) UNIQUE NOT NULL,
    teamId integer NOT NULL,

    INDEX (mobile),
    INDEX (email),
    INDEX (id),
    INDEX (teamId)
);

-- Team table:
CREATE TABLE teams
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    name varchar(50) NOT NULL,
    isCollege boolean NULL,
    isProfessional boolean NULL,
    city varchar(50) NOT NULL,
    state varchar(50) NOT NULL,
    country varchar(50) NOT NULL,
    generalManagerID integer NOT NULL,
    coachID integer NOT NULL,
    salaryCap integer NOT NULL,

    FOREIGN KEY (coachID) REFERENCES coaches (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (generalManagerID) REFERENCES general_managers (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    index (id)
);

-- Injuries table:
CREATE TABLE injuries
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    playerId integer NOT NULL,
    injuryDate date NOT NULL,
    recoveryDate date NOT NULL,
    description varchar(100) NOT NULL,

    INDEX (id),
    INDEX (playerId)
);

-- Player table:
CREATE TABLE players
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    firstName varchar(50) NOT NULL,
    middleName varchar(50),
    lastName varchar(50) NOT NULL,
    agentId integer NOT NULL,
    position varchar(50) NOT NULL,
    teamId integer NOT NULL,
    height integer NOT NULL,
    weight integer NOT NULL,
    dob date NOT NULL,
    injuryId integer NULL,

    FOREIGN KEY (agentId) REFERENCES agents (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (teamId) REFERENCES teams (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (injuryId) REFERENCES injuries (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    index (id),
    index (agentId),
    index (teamId)
);

-- Matches table:
CREATE TABLE matches
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    homeTeamId integer NOT NULL,
    awayTeamId integer NOT NULL,
    date date NOT NULL,
    time time NOT NULL,
    location varchar(50) NOT NULL,
    homeScore integer NOT NULL,
    awayScore integer NOT NULL,
    finalScore varchar(50) NOT NULL,

    FOREIGN KEY (homeTeamId) REFERENCES teams (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (awayTeamId) REFERENCES teams (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id),
    INDEX (homeTeamId),
    INDEX (awayTeamId)
);

-- Game plans table:
CREATE TABLE gameplans
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    matchId  integer NOT NULL,
    coachId  integer NOT NULL,
    planDate date NOT NULL,
    content varchar(50) NOT NULL,

    FOREIGN KEY (matchId) REFERENCES matches (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (coachId) REFERENCES coaches (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id),
    INDEX (coachId),
    INDEX (matchId)
);

-- Stats table:
CREATE TABLE statistics
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    playerId integer NOT NULL,
    matchId integer NOT NULL,
    totalPoints integer NOT NULL,
    fieldGoals integer NOT NULL,
    threePointers integer NOT NULL,
    steals integer NOT NULL,
    blocks integer NOT NULL,
    rebounds integer NOT NULL,
    assists integer NOT NULL,
    turnovers integer NOT NULL,
    freeThrows integer NOT NULL,
    totalPlayTime time NOT NULL,
    fouls integer NOT NULL,

    FOREIGN KEY (playerId) REFERENCES players (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (matchId) REFERENCES matches (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id),
    INDEX (playerId),
    INDEX (matchId)
);

-- reports table
CREATE TABLE reports
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    authorId integer NOT NULL,
    reportDate date NOT NULL,
    content varchar(50) NOT NULL,
    playerId integer NULL,           -- Nullable to handle scout reports without player association
    matchId integer NULL,            -- Nullable to handle scout reports without match association
    playerRating integer NULL,       -- Nullable to handle non-scout reports
    reportType enum('general', 'scout') NOT NULL,  -- Differentiates between general reports and scout reports

    FOREIGN KEY (authorId) REFERENCES users (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (playerId) REFERENCES players (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (matchId) REFERENCES matches (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id),
    INDEX (authorId),
    INDEX (playerId),
    INDEX (matchId)
);

-- Insertings values for each table
INSERT INTO users (firstName, middleName, lastName, mobile, email, role)
VALUES('Alex', NULL, 'Montgomery', '908-324-9005', 'Alex_Montgomery@gmail.com', 'system administrator'),
      ('Patrick', 'James', 'Carter', '732-735-7372', 'PJCarter.73@gmail.com', 'general manager'),
      ('Phillip', 'Robin', 'Smith', '508-564-1024', 'Psmith_10@yahoo.com', 'data analyst'),
      ('Mark', NULL, 'Hansen', '332-677-2124', 'mark.hansen@gmail.com', 'coach');

INSERT INTO agents (firstName, middleName, lastName, mobile, email)
VALUES('Liam', NULL, 'Kerney', '233-291-2034', 'liam_kerney67@gmail.com'),
      ('Jimmy', 'Falcon', 'Carter', '210-395-3922', 'jf.carter21@gmail.com');

INSERT INTO coaches (firstName, middleName, lastName, mobile, email, teamId, agentId)
VALUES ('Mike', 'Damon', 'Thompson', '556-677-8899', 'mike.thompson@gmail.com', 1, 1),
       ('Eric', 'Quan', 'Song', '923-200-0001', 'eric.qsong@gmail.com', 2, 2);

INSERT INTO general_managers (firstName, middleName, lastName, mobile, email, teamId)
VALUES ('Robert', 'Evan', 'Jones', '667-788-9900', 'robert.jones@yahoo.com', 1),
       ('Roger', 'Emmet', 'Fynes', '667-788-9900', 'roger.fynes@yahoo.com', 2);

INSERT INTO teams (name, isCollege, isProfessional, city, state, country, generalManagerID, coachID, salaryCap)
VALUES ('Los Angeles Lakers', 0, 1, 'Los Angeles', 'California', 'USA', 1, 1, 10000000),
       ('Boston Celtics', 0, 1, 'Boston', 'Massachusetts', 'USA', 2, 2, 10000500);

INSERT INTO injuries (playerId, injuryDate, recoveryDate, description)
VALUES (1, '2024-03-01', '2024-03-15', 'Sprained ankle'),
       (2, '2024-03-20', '2024-04-05', 'Knee injury'),
       (2, '2024-04-15', '2024-04-21', 'Broken Finger');

INSERT INTO players (firstName, middleName, lastName, agentId, position, teamId, height, weight, dob, injuryId)
VALUES ('James', 'Frank', 'Harden', 1, 'Point Guard', 1, 195, 200, '1993-08-26', 1),
       ('Jerome', 'Oliver', 'Rodrigo', 2, 'Power Foreward', 2, 211, 220, '1993-09-20', 2);

INSERT INTO matches (homeTeamId, awayTeamId, date, time, location, homeScore, awayScore, finalScore)
VALUES (1, 2, '2024-11-30', '19:00:00', 'LA Arena', 102, 98, '102-98'),
       (2, 1, '2025-03-08', '19:00:00', 'Boston Stadium', 111, 101, '111-101');

INSERT INTO gameplans (matchId, coachId, planDate, content)
VALUES (1, 1, '2024-11-29', 'Focus on fast breaks and defensive rebounds....'),
       (2, 2, '2025-03-05', 'Emphasize perimeter defense and ball movement.....');

INSERT INTO statistics (playerId, matchId, totalPoints, fieldGoals, threePointers, steals, blocks, rebounds, assists, turnovers, freeThrows, totalPlayTime, fouls)
VALUES (1, 1, 27, 11, 3, 2, 1, 5, 4, 3, 2, '00:38:00', 1),
       (1, 2, 23, 9, 3, 2, 4, 5, 3, 1, 2, '00:35:00', 0),
       (2, 1, 31, 12, 6, 3, 0, 6, 4, 5, 1, '00:35:00', 2),
       (2, 2, 17, 7, 2, 3, 0, 8, 2, 4, 1, '00:38:00', 1);

INSERT INTO reports (authorId, reportDate, content, playerId, matchId, playerRating, reportType)
VALUES
(1, '2024-11-30', 'LA vs Boston - Sys admin POV', NULL, NULL, NULL, 'general'),
(2, '2024-11-30', 'LA vs Boston - GM POV', NULL, NULL, NULL, 'general'),
(3, '2025-03-08', 'Boston vs LA - Data Analyst POV', NULL, NULL, NULL, 'general'),
(1, '2024-11-30', 'Excellent offensive efficiency with 27 points.', 1, 1, 8, 'scout'),
(2, '2024-11-30', 'Strong leadership in the game with 27 points.', 1, 1, 7, 'scout'),
(3, '2024-11-30', 'Data analysis shows Player #9 was efficient.', 1, 1, 7, 'scout'),
(1, '2024-11-30', 'Displayed excellent all-round capabilities.', 2, 1, 9, 'scout'),
(2, '2024-11-30', 'The player exhibited a great leadership.', 2, 1, 9, 'scout'),
(3, '2024-11-30', 'Efficient performance, 31 points, few fouls.', 2, 1, 9, 'scout'),
(1, '2025-03-08', 'Scored 23 points, solid efficiency.', 1, 2, 7, 'scout'),
(2, '2025-03-08', 'Scored 23 points, ok leadership, improve defense.', 1, 2, 6, 'scout'),
(3, '2025-03-08', 'Showed solid offense, improve turnovers.', 1, 2, 6, 'scout'),
(1, '2025-03-08', 'Scored 17 points, optimize efficiency.', 2, 2, 7, 'scout'),
(2, '2025-03-08', 'Fair leadership, improve consistency.', 2, 2, 6, 'scout'),
(3, '2025-03-08', '7 field goals and deceny PT, improve consistency.', 2, 2, 6, 'scout');