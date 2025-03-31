DROP DATABASE IF EXISTS DUNK_DETECTOR;
CREATE DATABASE IF NOT EXISTS DUNK_DETECTOR;

USE DUNK_DETECTOR;

# User table:
CREATE TABLE users
(
    id         integer AUTO_INCREMENT PRIMARY KEY,
    firstName  varchar(50)                                                               NOT NULL,
    middleName varchar(50),
    lastName   varchar(50)                                                               NOT NULL,
    mobile     varchar(15),
    email      varchar(75) UNIQUE                                                        NOT NULL,
    role       enum ('admin', 'agent', 'player', 'system administrator', 'data analyst') NOT NULL, # Adjust as needed

    INDEX (mobile),
    INDEX (email),
    INDEX (id)
);

# Team table:
CREATE TABLE teams
(
    id               integer AUTO_INCREMENT PRIMARY KEY,
    name             varchar(50)  NOT NULL,
    isCollege        boolean      NULL,
    isProfessional   boolean      NULL,
    city             varchar(50)  NOT NULL,
    state            varchar(50)  NOT NULL,
    country          varchar(50)  NOT NULL,
    generalManagerID integer      NOT NULL,
    coachID          integer      NOT NULL,
    salaryCap        integer      NOT NULL,
    playerRoster     varchar(100) NOT NULL, # Might need to consider alternative way of listing player

    FOREIGN KEY (generalManagerID) REFERENCES general_managers (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (coachID) REFERENCES coaches (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    index (id)
);

# Agent table:
CREATE TABLE agents
(
    id         integer AUTO_INCREMENT PRIMARY KEY,
    firstName  varchar(50)        NOT NULL,
    middleName varchar(50),
    lastName   varchar(50)        NOT NULL,
    mobile     varchar(15),
    email      varchar(75) UNIQUE NOT NULL,

    INDEX (mobile),
    INDEX (email),
    INDEX (id)
);

# General Manager table:
CREATE TABLE general_managers
(
    id         integer AUTO_INCREMENT PRIMARY KEY,
    firstName  varchar(50)        NOT NULL,
    middleName varchar(50),
    lastName   varchar(50)        NOT NULL,
    mobile     varchar(15),
    email      varchar(75) UNIQUE NOT NULL,
    teamId     integer            NOT NULL,

    FOREIGN KEY (teamId) REFERENCES teams (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (mobile),
    INDEX (email),
    INDEX (id),
    INDEX (teamId)
);

# Coach table:
CREATE TABLE coaches
(
    id         integer AUTO_INCREMENT PRIMARY KEY,
    firstName  varchar(50)        NOT NULL,
    middleName varchar(50),
    lastName   varchar(50)        NOT NULL,
    mobile     varchar(15),
    email      varchar(75) UNIQUE NOT NULL,
    teamId     integer            NOT NULL,
    agentId    integer            NOT NULL,

    FOREIGN KEY (teamId) REFERENCES teams (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    FOREIGN KEY (agentId) REFERENCES agents (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (mobile),
    INDEX (email),
    INDEX (id),
    INDEX (teamId)
);

# Player table:
CREATE TABLE players
(
    id         integer AUTO_INCREMENT PRIMARY KEY,
    firstName  varchar(50) NOT NULL,
    middleName varchar(50),
    lastName   varchar(50) NOT NULL,
    agentId    integer     NOT NULL,
    position   varchar(50) NOT NULL,
    teamId     integer     NOT NULL,
    height     integer     NOT NULL,
    weight     integer     NOT NULL,
    dob        date        NOT NULL,
    injuryId   integer     NOT NULL,

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

# Matches table:
CREATE TABLE matches
(
    id         integer AUTO_INCREMENT PRIMARY KEY,
    homeTeamId integer     NOT NULL,
    awayTeamId integer     NOT NULL,
    date       date        NOT NULL,
    time       time        NOT NULL,
    location   varchar(50) NOT NULL,
    winnerId   integer     NOT NULL,
    loserId    integer     NOT NULL,
    finalScore varchar(50) NOT NULL,

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

    INDEX (id),
    INDEX (homeTeamId),
    INDEX (awayTeamId),
    INDEX (winnerId),
    INDEX (loserId)
);

# Game plans table:
CREATE TABLE gameplans
(
    id       integer AUTO_INCREMENT PRIMARY KEY,
    matchId  integer        NOT NULL,
    coachId  integer        NOT NULL,
    planDate date           NOT NULL,
    content      varchar(50) NOT NULL,

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

# Stats table:
CREATE TABLE statistics
(
    id            integer AUTO_INCREMENT PRIMARY KEY,
    playerId      integer NOT NULL,
    matchId       integer NOT NULL,
    totalPoints   integer NOT NULL,
    fieldGoals    integer NOT NULL,
    threePointers integer NOT NULL,
    steals        integer NOT NULL,
    blocks        integer NOT NULL,
    rebounds      integer NOT NULL,
    assists       integer NOT NULL,
    turnovers     integer NOT NULL,
    freeThrows    integer NOT NULL,
    totalPlayTime time    NOT NULL,
    fouls         integer NOT NULL,

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

# Injuries table:
CREATE TABLE injuries
(
    id           integer AUTO_INCREMENT PRIMARY KEY,
    playerId     integer      NOT NULL,
    injuryDate   date         NOT NULL,
    recoveryDate date         NOT NULL,
    description  varchar(100) NOT NULL,

    FOREIGN KEY (playerId) REFERENCES players (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id),
    INDEX (playerId)
);

# Reports table:
CREATE TABLE reports
(
    id         integer AUTO_INCREMENT PRIMARY KEY,
    authorId   integer        NOT NULL, # should this reference userID?
    reportDate date           NOT NULL,
    content      varchar(50) NOT NULL,

    FOREIGN KEY (authorId) REFERENCES users (id)
        ON UPDATE RESTRICT
        ON DELETE CASCADE,

    INDEX (id),
    INDEX (authorId)
);

# Scout reports table:
CREATE TABLE scout_reports
(
    id           integer AUTO_INCREMENT PRIMARY KEY,
    authorId     integer        NOT NULL, # should this reference userID?
    playerId     integer        NOT NULL,
    matchId      integer        NOT NULL,
    reportDate   date           NOT NULL,
    content      varchar(50) NOT NULL,
    playerRating integer        NOT NULL,

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
    INDEX (playerId)
);