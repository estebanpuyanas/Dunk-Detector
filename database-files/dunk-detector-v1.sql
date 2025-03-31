DROP DATABASE IF EXISTS dunkDetector;
CREATE DATABASE IF NOT EXISTS dunkDetector;

USE dunkDetector;

# Users table:
CREATE TABLE users
(
    id         INTEGER AUTO_INCREMENT PRIMARY KEY,
    firstName  VARCHAR(50) NOT NULL,
    middleName VARCHAR(50),
    lastName   VARCHAR(50) NOT NULL,
    mobile     VARCHAR(15),
    email      VARCHAR(75) UNIQUE NOT NULL,
    role       ENUM ('admin', 'agent', 'player', 'system administrator', 'data analyst') NOT NULL,

    INDEX (mobile),
    INDEX (email),
    INDEX (id)
);

# Agents table:
CREATE TABLE agents
(
    id         INTEGER AUTO_INCREMENT PRIMARY KEY,
    firstName  VARCHAR(50) NOT NULL,
    middleName VARCHAR(50),
    lastName   VARCHAR(50) NOT NULL,
    mobile     VARCHAR(15),
    email      VARCHAR(75) UNIQUE NOT NULL,

    INDEX (mobile),
    INDEX (email),
    INDEX (id)
);

# General Managers table (Initially without teamId foreign key)
CREATE TABLE general_managers
(
    id         INTEGER AUTO_INCREMENT PRIMARY KEY,
    firstName  VARCHAR(50) NOT NULL,
    middleName VARCHAR(50),
    lastName   VARCHAR(50) NOT NULL,
    mobile     VARCHAR(15),
    email      VARCHAR(75) UNIQUE NOT NULL,
    teamId     INTEGER NULL,  # Will be added later

    INDEX (mobile),
    INDEX (email),
    INDEX (teamId),
    INDEX (id)
);

# Coaches table (Initially without teamId foreign key)
CREATE TABLE coaches
(
    id         INTEGER AUTO_INCREMENT PRIMARY KEY,
    firstName  VARCHAR(50) NOT NULL,
    middleName VARCHAR(50),
    lastName   VARCHAR(50) NOT NULL,
    mobile     VARCHAR(15),
    email      VARCHAR(75) UNIQUE NOT NULL,
    teamId     INTEGER NULL,  # Will be added later
    agentId    INTEGER NOT NULL,

    FOREIGN KEY (agentId) REFERENCES agents (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (mobile),
    INDEX (email),
    INDEX (teamId),
    INDEX (id)
);

# Teams table (Initially without foreign key constraints)
CREATE TABLE teams
(
    id             INTEGER AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(50) NOT NULL,
    isCollege      BOOLEAN,
    isProfessional BOOLEAN,
    city           VARCHAR(50) NOT NULL,
    state          VARCHAR(50) NOT NULL,
    country        VARCHAR(50) NOT NULL,
    generalManagerID INTEGER NULL,  # Will be added later
    coachID        INTEGER NULL,  # Will be added later
    salaryCap      INTEGER NOT NULL,
    playerRoster   VARCHAR(100) NOT NULL,

    INDEX (id)
);

# Players table (Initially with injuryId set to NULL)
CREATE TABLE players
(
    id         INTEGER AUTO_INCREMENT PRIMARY KEY,
    firstName  VARCHAR(50) NOT NULL,
    middleName VARCHAR(50),
    lastName   VARCHAR(50) NOT NULL,
    agentId    INTEGER NOT NULL,
    position   VARCHAR(50) NOT NULL,
    teamId     INTEGER NOT NULL,
    height     INTEGER NOT NULL,
    weight     INTEGER NOT NULL,
    dob        DATE NOT NULL,
    injuryId   INTEGER NULL,  # Will be added later

    FOREIGN KEY (agentId) REFERENCES agents (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (teamId) REFERENCES teams (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id)
);

# Injuries table (Initially without playerId constraint)
CREATE TABLE injuries
(
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    playerId INTEGER NULL,  # Will be added later
    injuryDate DATE NOT NULL,
    recoveryDate DATE NOT NULL,
    description VARCHAR(100) NOT NULL,

    INDEX (id),
    INDEX (playerId)
);

# Matches table:
CREATE TABLE matches
(
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    homeTeamId INTEGER NOT NULL,
    awayTeamId INTEGER NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    location VARCHAR(50) NOT NULL,
    winnerId INTEGER NOT NULL,
    loserId INTEGER NOT NULL,
    finalScore VARCHAR(50) NOT NULL,

    FOREIGN KEY (homeTeamId) REFERENCES teams (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (awayTeamId) REFERENCES teams (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (winnerId) REFERENCES teams (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (loserId) REFERENCES teams (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id)
);

# Scout Reports table:
CREATE TABLE scout_reports
(
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    authorId INTEGER NOT NULL,
    playerId INTEGER NOT NULL,
    date DATE NOT NULL,
    content VARCHAR(50) NOT NULL,
    matchId INTEGER NOT NULL,

    FOREIGN KEY (playerId) REFERENCES players (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (matchId) REFERENCES matches (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (authorId) REFERENCES users (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id)
);

# Game plans table:
CREATE TABLE game_plans
(
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    matchId  INTEGER NOT NULL,
    coachId  INTEGER NOT NULL,
    planDate DATE NOT NULL,
    content  VARCHAR(50) NOT NULL,

    FOREIGN KEY (matchId) REFERENCES matches (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (coachId) REFERENCES coaches (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id)
);

CREATE TABLE statistics
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    playerId integer NOT NULL,
    matchId  integer NOT NULL,
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

# Reports table:
CREATE TABLE reports
(
    id integer AUTO_INCREMENT PRIMARY KEY,
    authorId   integer NOT NULL, # should this reference userID?
    reportDate date NOT NULL,
    content varchar(50) NOT NULL,

    FOREIGN KEY (authorId) REFERENCES users (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id),
    INDEX (authorId)
);

# Adding Foreign Key Constraints After Table Creation
ALTER TABLE teams ADD FOREIGN KEY (generalManagerID) REFERENCES general_managers (id)
    ON UPDATE RESTRICT
    ON DELETE CASCADE;

ALTER TABLE teams ADD FOREIGN KEY (coachID) REFERENCES coaches (id)
    ON UPDATE RESTRICT
    ON DELETE CASCADE;

ALTER TABLE general_managers ADD FOREIGN KEY (teamId) REFERENCES teams (id)
    ON UPDATE RESTRICT
    ON DELETE CASCADE;

ALTER TABLE coaches ADD FOREIGN KEY (teamId) REFERENCES teams (id)
    ON UPDATE RESTRICT
    ON DELETE CASCADE;

ALTER TABLE players ADD FOREIGN KEY (injuryId) REFERENCES injuries (id)
    ON UPDATE RESTRICT
    ON DELETE CASCADE;

ALTER TABLE injuries ADD FOREIGN KEY (playerId) REFERENCES players (id)
    ON UPDATE RESTRICT
    ON DELETE CASCADE;