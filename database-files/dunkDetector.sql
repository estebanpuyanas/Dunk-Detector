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
    image blob,

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

INSERT INTO agents (firstName, middleName, lastName, mobile, email)
VALUES ('Michael', 'A.', 'Johnson', '555000001', 'michael.johnson@example.com'),
       ('James', 'B.', 'Smith', '555000002', 'james.smith@example.com'),
       ('Robert', NULL, 'Williams', '555000003', 'robert.williams@example.com'),
       ('John', 'C.', 'Brown', '555000004', 'john.brown@example.com'),
       ('David', NULL, 'Jones', '555000005', 'david.jones@example.com'),
       ('William', 'D.', 'Garcia', '555000006', 'william.garcia@example.com'),
       ('Richard', NULL, 'Miller', '555000007', 'richard.miller@example.com'),
       ('Joseph', 'E.', 'Davis', '555000008', 'joseph.davis@example.com'),
       ('Thomas', NULL, 'Rodriguez', '555000009', 'thomas.rodriguez@example.com'),
       ('Charles', 'F.', 'Martinez', '555000010', 'charles.martinez@example.com'),
       ('Christopher', NULL, 'Hernandez', '555000011', 'christopher.hernandez@example.com'),
       ('Daniel', 'G.', 'Lopez', '555000012', 'daniel.lopez@example.com'),
       ('Matthew', NULL, 'Gonzalez', '555000013', 'matthew.gonzalez@example.com'),
       ('Anthony', 'H.', 'Wilson', '555000014', 'anthony.wilson@example.com'),
       ('Mark', NULL, 'Anderson', '555000015', 'mark.anderson@example.com'),
       ('Donald', 'I.', 'Thomas', '555000016', 'donald.thomas@example.com'),
       ('Steven', NULL, 'Taylor', '555000017', 'steven.taylor@example.com'),
       ('Paul', 'J.', 'Moore', '555000018', 'paul.moore@example.com'),
       ('Andrew', NULL, 'Jackson', '555000019', 'andrew.jackson@example.com'),
       ('Joshua', 'K.', 'Martin', '555000020', 'joshua.martin@example.com');

INSERT INTO general_managers (firstName, middleName, lastName, mobile, email, teamId)
VALUES ('George', 'L.', 'King', '555100001', 'george.king@example.com', 1),
       ('Edward', NULL, 'Scott', '555100002', 'edward.scott@example.com', 2),
       ('Henry', 'M.', 'Adams', '555100003', 'henry.adams@example.com', 3),
       ('Samuel', NULL, 'Baker', '555100004', 'samuel.baker@example.com', 4),
       ('Arthur', 'N.', 'Nelson', '555100005', 'arthur.nelson@example.com', 5),
       ('Benjamin', NULL, 'Carter', '555100006', 'benjamin.carter@example.com', 6),
       ('Lucas', 'O.', 'Mitchell', '555100007', 'lucas.mitchell@example.com', 7),
       ('Oliver', NULL, 'Perez', '555100008', 'oliver.perez@example.com', 8),
       ('Elijah', 'P.', 'Roberts', '555100009', 'elijah.roberts@example.com', 9),
       ('Mason', NULL, 'Turner', '555100010', 'mason.turner@example.com', 10),
       ('Logan', 'Q.', 'Phillips', '555100011', 'logan.phillips@example.com', 11),
       ('Jacob', NULL, 'Campbell', '555100012', 'jacob.campbell@example.com', 12),
       ('Ethan', 'R.', 'Parker', '555100013', 'ethan.parker@example.com', 13),
       ('Michael', NULL, 'Evans', '555100014', 'michael.evans@example.com', 14),
       ('Alexander', 'S.', 'Edwards', '555100015', 'alexander.edwards@example.com', 15),
       ('Daniel', 'T.', 'Collins', '555100016', 'daniel.collins@example.com', 16),
       ('Matthew', NULL, 'Stewart', '555100017', 'matthew.stewart@example.com', 17),
       ('Joseph', 'U.', 'Sanchez', '555100018', 'joseph.sanchez@example.com', 18),
       ('David', NULL, 'Morris', '555100019', 'david.morris@example.com', 19),
       ('Samuel', 'V.', 'Rogers', '555100020', 'samuel.rogers@example.com', 20);

INSERT INTO coaches (firstName, middleName, lastName, mobile, email, teamId, agentId)
VALUES ('Brian', 'L.', 'Edwards', '555200001', 'brian.edwards@example.com', 1, 1),
       ('Timothy', NULL, 'Murphy', '555200002', 'timothy.murphy@example.com', 2, 2),
       ('Kevin', 'M.', 'Richardson', '555200003', 'kevin.richardson@example.com', 3, 3),
       ('Steven', NULL, 'Peterson', '555200004', 'steven.peterson@example.com', 4, 4),
       ('Eric', 'N.', 'Howard', '555200005', 'eric.howard@example.com', 5, 5),
       ('Mark', 'O.', 'Jenkins', '555200006', 'mark.jenkins@example.com', 6, 6),
       ('Charles', NULL, 'Russell', '555200007', 'charles.russell@example.com', 7, 7),
       ('Patrick', 'P.', 'Griffin', '555200008', 'patrick.griffin@example.com', 8, 8),
       ('Scott', 'Q.', 'Patterson', '555200009', 'scott.patterson@example.com', 9, 9),
       ('Jason', NULL, 'Simmons', '555200010', 'jason.simmons@example.com', 10, 10),
       ('Greg', 'R.', 'Barnes', '555200011', 'greg.barnes@example.com', 11, 11),
       ('Paul', NULL, 'Fisher', '555200012', 'paul.fisher@example.com', 12, 12),
       ('Ryan', 'S.', 'Harvey', '555200013', 'ryan.harvey@example.com', 13, 13),
       ('Larry', NULL, 'Hamilton', '555200014', 'larry.hamilton@example.com', 14, 14),
       ('Scott', 'T.', 'Wallace', '555200015', 'scott.wallace@example.com', 15, 15),
       ('Frank', 'U.', 'Woods', '555200016', 'frank.woods@example.com', 16, 16),
       ('Peter', 'V.', 'West', '555200017', 'peter.west@example.com', 17, 17),
       ('Andrew', NULL, 'Cole', '555200018', 'andrew.cole@example.com', 18, 18),
       ('Benjamin', 'W.', 'Hunter', '555200019', 'benjamin.hunter@example.com', 19, 19),
       ('Gregory', NULL, 'Stone', '555200020', 'gregory.stone@example.com', 20, 20);

INSERT INTO teams (id, name, isCollege, isProfessional, city, state, country, generalManagerID, coachID, salaryCap)
VALUES (1, 'Capitals', TRUE, FALSE, 'Boston', 'MA', 'USA', 1, 1, 5000000),
       (2, 'Cavaliers', TRUE, FALSE, 'Newark', 'NJ', 'USA', 2, 2, 5200000),
       (3, 'Spartans', TRUE, FALSE, 'Philadelphia', 'PA', 'USA', 3, 3, 5400000),
       (4, 'Eagles', TRUE, FALSE, 'Providence', 'RI', 'USA', 4, 4, 5600000),
       (5, 'Titans', TRUE, FALSE, 'Cambridge', 'MA', 'USA', 5, 5, 5800000),
       (6, 'Warriors', TRUE, FALSE, 'Pittsburgh', 'PA', 'USA', 6, 6, 6000000),
       (7, 'Comets', TRUE, FALSE, 'Baltimore', 'MD', 'USA', 7, 7, 6200000),
       (8, 'Hurricanes', TRUE, FALSE, 'Miami', 'FL', 'USA', 8, 8, 6400000),
       (9, 'Mountaineers', TRUE, FALSE, 'Denver', 'CO', 'USA', 9, 9, 6600000),
       (10, 'Rams', TRUE, FALSE, 'Sacramento', 'CA', 'USA', 10, 10, 6800000),
       (11, 'Lions', FALSE, TRUE, 'Los Angeles', 'CA', 'USA', 11, 11, 90000000),
       (12, 'Bulls', FALSE, TRUE, 'Chicago', 'IL', 'USA', 12, 12, 92000000),
       (13, 'Knights', FALSE, TRUE, 'Houston', 'TX', 'USA', 13, 13, 94000000),
       (14, 'Pirates', FALSE, TRUE, 'San Francisco', 'CA', 'USA', 14, 14, 96000000),
       (15, 'Dragons', FALSE, TRUE, 'Phoenix', 'AZ', 'USA', 15, 15, 98000000),
       (16, 'Rangers', FALSE, TRUE, 'Dallas', 'TX', 'USA', 16, 16, 100000000),
       (17, 'Falcons', FALSE, TRUE, 'Atlanta', 'GA', 'USA', 17, 17, 102000000),
       (18, 'Vikings', FALSE, TRUE, 'Minneapolis', 'MN', 'USA', 18, 18, 104000000),
       (19, 'Knicks', FALSE, TRUE, 'New York', 'NY', 'USA', 19, 19, 106000000),
       (20, 'Giants', FALSE, TRUE, 'San Diego', 'CA', 'USA', 20, 20, 108000000);

INSERT INTO users (firstName, middleName, lastName, mobile, email, role)
VALUES ('Alice', NULL, 'Walker', '555300001', 'alice.walker@example.com', 'admin'),
       ('Bob', 'T.', 'Harris', '555300002', 'bob.harris@example.com', 'data analyst'),
       ('Carol', NULL, 'Young', '555300003', 'carol.young@example.com', 'system administrator'),
       ('David', 'P.', 'Hall', '555300004', 'david.hall@example.com', 'general manager'),
       ('Emma', 'Q.', 'Allen', '555300005', 'emma.allen@example.com', 'coach'),
       ('Frank', NULL, 'Wright', '555300006', 'frank.wright@example.com', 'player'),
       ('Grace', 'R.', 'Scott', '555300007', 'grace.scott@example.com', 'agent'),
       ('Henry', NULL, 'King', '555300008', 'henry.king@example.com', 'player'),
       ('Irene', 'S.', 'Green', '555300009', 'irene.green@example.com', 'coach'),
       ('Jack', NULL, 'Baker', '555300010', 'jack.baker@example.com', 'agent'),
       ('Karen', 'U.', 'Nelson', '555300011', 'karen.nelson@example.com', 'system administrator'),
       ('Leo', NULL, 'Carter', '555300012', 'leo.carter@example.com', 'data analyst'),
       ('Mia', 'V.', 'Mitchell', '555300013', 'mia.mitchell@example.com', 'player'),
       ('Noah', NULL, 'Perez', '555300014', 'noah.perez@example.com', 'general manager'),
       ('Olivia', 'W.', 'Roberts', '555300015', 'olivia.roberts@example.com', 'coach'),
       ('Paul', NULL, 'Turner', '555300016', 'paul.turner@example.com', 'admin'),
       ('Quinn', 'X.', 'Phillips', '555300017', 'quinn.phillips@example.com', 'player'),
       ('Rachel', NULL, 'Campbell', '555300018', 'rachel.campbell@example.com', 'agent'),
       ('Steve', 'Y.', 'Parker', '555300019', 'steve.parker@example.com', 'data analyst'),
       ('Tina', NULL, 'Evans', '555300020', 'tina.evans@example.com', 'general manager'),
       ('Uma', 'Z.', 'Edwards', '555300021', 'uma.edwards@example.com', 'coach'),
       ('Victor', NULL, 'Collins', '555300022', 'victor.collins@example.com', 'player'),
       ('Wendy', 'A.', 'Stewart', '555300023', 'wendy.stewart@example.com', 'admin'),
       ('Xavier', NULL, 'Sanchez', '555300024', 'xavier.sanchez@example.com', 'agent'),
       ('Yvonne', 'B.', 'Morris', '555300025', 'yvonne.morris@example.com', 'system administrator'),
       ('Zach', NULL, 'Rogers', '555300026', 'zach.rogers@example.com', 'data analyst'),
       ('Aaron', 'C.', 'Reed', '555300027', 'aaron.reed@example.com', 'player'),
       ('Bella', NULL, 'Cook', '555300028', 'bella.cook@example.com', 'general manager'),
       ('Carter', 'D.', 'Morgan', '555300029', 'carter.morgan@example.com', 'coach'),
       ('Diana', NULL, 'Bell', '555300030', 'diana.bell@example.com', 'player');

INSERT INTO players (firstName, middleName, lastName, agentId, position, teamId, height, weight, dob, injuryId)
VALUES ('Ethan', 'F.', 'Brown', 1, 'Point Guard', 1, 74, 180, '1995-06-15', NULL),
       ('Liam', NULL, 'Smith', 2, 'Shooting Guard', 2, 76, 190, '1997-08-21', NULL),
       ('Mason', 'G.', 'Johnson', 3, 'Small Forward', 3, 78, 210, '1994-03-02', NULL),
       ('Logan', NULL, 'Williams', 4, 'Power Forward', 4, 80, 220, '1996-11-11', NULL),
       ('Lucas', 'H.', 'Jones', 5, 'Center', 5, 83, 240, '1998-02-28', NULL),
       ('Noah', NULL, 'Brown', 6, 'Point Guard', 6, 73, 175, '1999-07-07', NULL),
       ('Oliver', 'I.', 'Davis', 7, 'Shooting Guard', 7, 75, 185, '1993-12-12', NULL),
       ('Elijah', NULL, 'Miller', 8, 'Small Forward', 8, 77, 200, '1992-04-18', NULL),
       ('Aiden', 'J.', 'Wilson', 9, 'Power Forward', 9, 79, 215, '1995-09-09', NULL),
       ('Samuel', NULL, 'Moore', 10, 'Center', 10, 82, 230, '1991-10-10', NULL),
       ('Gabriel', 'K.', 'Taylor', 11, 'Point Guard', 11, 74, 180, '1996-05-05', NULL),
       ('Daniel', NULL, 'Anderson', 12, 'Shooting Guard', 12, 76, 190, '1997-06-06', NULL),
       ('Anthony', 'L.', 'Thomas', 13, 'Small Forward', 13, 78, 205, '1994-08-08', NULL),
       ('Joseph', NULL, 'Jackson', 14, 'Power Forward', 14, 80, 220, '1992-11-11', NULL),
       ('David', 'M.', 'White', 15, 'Center', 15, 83, 245, '1998-03-03', NULL),
       ('Carter', NULL, 'Harris', 16, 'Point Guard', 16, 73, 175, '1999-12-12', NULL),
       ('Owen', 'N.', 'Martin', 17, 'Shooting Guard', 17, 75, 185, '1995-01-01', NULL),
       ('Wyatt', NULL, 'Thompson', 18, 'Small Forward', 18, 77, 200, '1993-07-07', NULL),
       ('Jack', 'O.', 'Garcia', 19, 'Power Forward', 19, 79, 215, '1996-09-09', NULL),
       ('Luke', NULL, 'Martinez', 20, 'Center', 20, 82, 230, '1994-04-04', NULL),
       ('Henry', 'P.', 'Robinson', 1, 'Point Guard', 1, 74, 180, '1997-02-20', NULL),
       ('Levi', NULL, 'Clark', 2, 'Shooting Guard', 2, 76, 190, '1998-10-10', NULL),
       ('Sebastian', 'Q.', 'Rodriguez', 3, 'Small Forward', 3, 78, 210, '1995-05-15', NULL),
       ('Mateo', NULL, 'Lewis', 4, 'Power Forward', 4, 80, 220, '1996-06-16', NULL),
       ('Julian', 'R.', 'Lee', 5, 'Center', 5, 83, 240, '1993-07-17', NULL),
       ('Anthony', NULL, 'Walker', 6, 'Point Guard', 6, 73, 175, '1994-08-18', NULL),
       ('Isaiah', 'S.', 'Hall', 7, 'Shooting Guard', 7, 75, 185, '1992-09-19', NULL),
       ('Aaron', NULL, 'Allen', 8, 'Small Forward', 8, 77, 200, '1991-10-20', NULL),
       ('Eli', 'T.', 'Young', 9, 'Power Forward', 9, 79, 215, '1997-11-21', NULL),
       ('Oliver', NULL, 'Hernandez', 10, 'Center', 10, 82, 230, '1995-12-22', NULL);

INSERT INTO injuries (playerId, injuryDate, recoveryDate, description)
VALUES (2, '2023-01-10', '2023-02-10', 'Sprained ankle'),
       (5, '2022-12-05', '2023-01-15', 'Knee injury'),
       (7, '2023-03-20', '2023-04-20', 'Hamstring strain'),
       (11, '2023-02-25', '2023-03-25', 'Wrist sprain'),
       (14, '2023-04-01', '2023-05-01', 'Ankle sprain'),
       (20, '2022-11-15', '2022-12-15', 'Back pain'),
       (22, '2023-05-10', '2023-06-10', 'Concussion'),
       (3, '2023-01-20', '2023-02-20', 'Calf strain'),
       (8, '2022-10-05', '2022-11-05', 'Shoulder injury'),
       (10, '2023-03-15', '2023-04-15', 'Groin pull'),
       (13, '2023-02-12', '2023-03-12', 'Hamstring strain'),
       (16, '2023-04-20', '2023-05-20', 'Wrist sprain'),
       (17, '2023-05-01', '2023-06-01', 'Knee injury'),
       (18, '2023-01-05', '2023-02-05', 'Ankle sprain'),
       (21, '2023-02-15', '2023-03-15', 'Back strain'),
       (24, '2023-03-05', '2023-04-05', 'Hamstring injury'),
       (25, '2022-12-20', '2023-01-20', 'Shoulder strain'),
       (26, '2023-04-10', '2023-05-10', 'Calf injury'),
       (27, '2023-05-05', '2023-06-05', 'Knee sprain'),
       (28, '2023-02-28', '2023-03-28', 'Wrist fracture'),
       (29, '2023-01-30', '2023-02-28', 'Concussion'),
       (4, '2023-03-22', '2023-04-22', 'Ankle sprain'),
       (6, '2022-11-30', '2022-12-30', 'Knee injury'),
       (9, '2023-04-25', '2023-05-25', 'Hamstring strain'),
       (12, '2023-02-18', '2023-03-18', 'Back injury');

INSERT INTO matches (homeTeamId, awayTeamId, date, time, location, homeScore, awayScore, finalScore)
VALUES (1, 2, '2023-05-01', '19:00:00', 'Boston Arena', 78, 75, '78-75'),
       (3, 4, '2023-05-02', '20:00:00', 'Philadelphia Stadium', 85, 82, '85-82'),
       (5, 6, '2023-05-03', '18:30:00', 'Cambridge Court', 65, 70, '65-70'),
       (7, 8, '2023-05-04', '19:30:00', 'Baltimore Dome', 90, 88, '90-88'),
       (9, 10, '2023-05-05', '20:30:00', 'Denver Field', 102, 99, '102-99'),
       (11, 12, '2023-05-06', '21:00:00', 'Los Angeles Arena', 110, 105, '110-105'),
       (13, 14, '2023-05-07', '19:00:00', 'Houston Stadium', 95, 100, '95-100'),
       (15, 16, '2023-05-08', '18:00:00', 'Phoenix Dome', 88, 90, '88-90'),
       (17, 18, '2023-05-09', '20:15:00', 'Atlanta Arena', 76, 74, '76-74'),
       (19, 20, '2023-05-10', '21:30:00', 'New York Stadium', 102, 101, '102-101'),
       (2, 3, '2023-05-11', '19:45:00', 'Newark Center', 80, 79, '80-79'),
       (4, 5, '2023-05-12', '18:50:00', 'Providence Arena', 68, 72, '68-72'),
       (6, 7, '2023-05-13', '20:20:00', 'Pittsburgh Stadium', 85, 87, '85-87'),
       (8, 9, '2023-05-14', '19:10:00', 'Miami Court', 77, 75, '77-75'),
       (10, 1, '2023-05-15', '21:10:00', 'Sacramento Arena', 90, 85, '90-85'),
       (12, 11, '2023-05-16', '20:40:00', 'Chicago Stadium', 95, 92, '95-92'),
       (14, 13, '2023-05-17', '19:20:00', 'San Francisco Dome', 88, 90, '88-90'),
       (16, 15, '2023-05-18', '20:30:00', 'Dallas Court', 104, 99, '104-99'),
       (18, 17, '2023-05-19', '21:00:00', 'Minneapolis Stadium', 79, 80, '79-80'),
       (20, 19, '2023-05-20', '19:30:00', 'San Diego Arena', 88, 86, '88-86');

INSERT INTO gameplans (matchId, coachId, planDate, content, image)
VALUES (1, 1, '2023-04-30', 'Defensive focus', NULL),
       (2, 2, '2023-05-01', 'Fast break strategy', NULL),
       (3, 3, '2023-05-02', 'Zone defense', NULL),
       (4, 4, '2023-05-03', 'Pick and roll emphasis', NULL),
       (5, 5, '2023-05-04', 'Rebounding tactics', NULL),
       (6, 6, '2023-05-05', 'Full court press', NULL),
       (7, 7, '2023-05-06', 'Defensive rotations', NULL),
       (8, 8, '2023-05-07', 'Perimeter shooting', NULL),
       (9, 9, '2023-05-08', 'Man-to-man defense', NULL),
       (10, 10, '2023-05-09', 'Slow pace control', NULL),
       (11, 11, '2023-05-10', 'High press', NULL),
       (12, 12, '2023-05-11', 'Transition offense', NULL),
       (13, 13, '2023-05-12', 'Isolation plays', NULL),
       (14, 14, '2023-05-13', 'Defensive rebound', NULL),
       (15, 15, '2023-05-14', 'Fast break execution', NULL),
       (16, 16, '2023-05-15', 'Zone defense', NULL),
       (17, 17, '2023-05-16', 'Ball movement', NULL),
       (18, 18, '2023-05-17', 'Pick and roll', NULL),
       (19, 19, '2023-05-18', 'Perimeter defense', NULL),
       (20, 20, '2023-05-19', 'Structured offense', NULL);

INSERT INTO statistics (playerId, matchId, totalPoints, fieldGoals, threePointers, steals, blocks, rebounds, assists,
                        turnovers, freeThrows, totalPlayTime, fouls)
VALUES (1, 1, 15, 5, 2, 1, 0, 4, 3, 2, 3, '00:30:00', 2),
       (2, 2, 20, 7, 3, 2, 1, 5, 4, 1, 2, '00:32:00', 3),
       (3, 3, 12, 4, 1, 1, 0, 6, 2, 3, 2, '00:28:00', 1),
       (4, 4, 18, 6, 2, 2, 1, 7, 5, 2, 4, '00:33:00', 2),
       (5, 5, 22, 8, 3, 1, 2, 9, 4, 3, 3, '00:35:00', 3),
       (6, 6, 16, 5, 2, 1, 1, 8, 3, 2, 2, '00:31:00', 2),
       (7, 7, 14, 4, 1, 3, 1, 7, 3, 1, 1, '00:29:00', 1),
       (8, 8, 19, 6, 2, 2, 2, 10, 5, 2, 3, '00:34:00', 2),
       (9, 9, 11, 4, 0, 1, 0, 5, 2, 2, 2, '00:27:00', 1),
       (10, 10, 24, 9, 4, 2, 1, 11, 6, 3, 4, '00:36:00', 3),
       (11, 11, 17, 6, 2, 1, 1, 8, 5, 1, 3, '00:32:00', 2),
       (12, 12, 13, 5, 1, 2, 0, 7, 2, 2, 2, '00:30:00', 1),
       (13, 13, 21, 7, 3, 2, 1, 9, 4, 2, 3, '00:33:00', 2),
       (14, 14, 16, 5, 2, 1, 1, 8, 3, 1, 2, '00:31:00', 2),
       (15, 15, 23, 8, 3, 2, 2, 10, 5, 3, 4, '00:35:00', 3),
       (16, 16, 19, 7, 2, 1, 1, 9, 4, 2, 3, '00:33:00', 2),
       (17, 17, 14, 5, 1, 2, 1, 7, 3, 2, 2, '00:30:00', 1),
       (18, 18, 20, 7, 2, 2, 1, 8, 5, 3, 3, '00:32:00', 2),
       (19, 19, 18, 6, 2, 1, 1, 7, 4, 2, 2, '00:31:00', 2),
       (20, 20, 22, 8, 3, 2, 2, 10, 6, 3, 4, '00:34:00', 3);

INSERT INTO reports (authorId, reportDate, content, playerId, matchId, playerRating, reportType)
VALUES (1, '2023-05-05', 'Great performance in scoring.', 1, 1, 8, 'scout'),
       (2, '2023-05-06', 'Solid defense observed.', 2, 2, 7, 'scout'),
       (3, '2023-05-07', 'Needs improvement on ball control.', 3, 3, 6, 'scout'),
       (4, '2023-05-08', 'Exceptional playmaking.', 4, 4, 9, 'scout'),
       (5, '2023-05-09', 'Team showed great chemistry.', NULL, 5, NULL, 'general'),
       (6, '2023-05-10', 'Poor shooting accuracy.', 6, 6, 5, 'scout'),
       (7, '2023-05-11', 'Good overall athleticism.', 7, NULL, 8, 'scout'),
       (8, '2023-05-12', 'The game plan was effective.', NULL, 7, NULL, 'general'),
       (9, '2023-05-13', 'Struggled with turnovers.', 8, 8, 6, 'scout'),
       (10, '2023-05-14', 'Positive impact on defense.', 9, 9, 7, 'scout'),
       (11, '2023-05-15', 'Coach provided strong leadership.', NULL, 10, NULL, 'general'),
       (12, '2023-05-16', 'Player showed remarkable speed.', 10, 11, 8, 'scout'),
       (13, '2023-05-17', 'Inconsistent shooting noted.', 11, 12, 6, 'scout'),
       (14, '2023-05-18', 'Teamwork was evident throughout.', NULL, 13, NULL, 'general'),
       (15, '2023-05-19', 'Defensive adjustments needed.', 12, 14, 7, 'scout'),
       (16, '2023-05-20', 'Energetic performance from the bench.', NULL, 15, NULL, 'general'),
       (17, '2023-05-21', 'Player was pivotal in transition.', 13, 16, 8, 'scout'),
       (18, '2023-05-22', 'Excellent ball distribution.', 14, 17, 9, 'scout'),
       (19, '2023-05-23', 'Lacked defensive focus.', 15, 18, 6, 'scout'),
       (20, '2023-05-24', 'Overall, a balanced game.', NULL, 19, NULL, 'general');

USE dunkDetector;

-- 1) Add four new matches (IDs 21–24)
INSERT INTO matches (homeTeamId, awayTeamId, date, time, location, homeScore, awayScore, finalScore)
VALUES
  ( 2,  3, '2023-05-21', '19:00:00', 'City21 Arena',  88,  82, '88-82'),
  ( 4,  5, '2023-05-22', '20:00:00', 'City22 Arena',  95,  90, '95-90'),
  ( 6,  7, '2023-05-23', '18:30:00', 'City23 Arena',  78,  80, '78-80'),
  ( 8,  9, '2023-05-24', '19:30:00', 'City24 Arena', 102,  99, '102-99');

-- 2) For each of those matches, insert one stats row per player (IDs 1–30)
--    using INSERT…SELECT from players with RAND() for variety.

INSERT INTO statistics (
  playerId, matchId,
  totalPoints, fieldGoals, threePointers,
  steals, blocks, rebounds,
  assists, turnovers, freeThrows,
  totalPlayTime, fouls
)
SELECT
  id, 21,
  FLOOR(RAND()*35), FLOOR(RAND()*15), FLOOR(RAND()*10),
  FLOOR(RAND()*5), FLOOR(RAND()*3), FLOOR(RAND()*12),
  FLOOR(RAND()*10), FLOOR(RAND()*5), FLOOR(RAND()*10),
  SEC_TO_TIME(1800 + FLOOR(RAND()*1200)),
  FLOOR(RAND()*6)
FROM players;

INSERT INTO statistics (
  playerId, matchId,
  totalPoints, fieldGoals, threePointers,
  steals, blocks, rebounds,
  assists, turnovers, freeThrows,
  totalPlayTime, fouls
)
SELECT
  id, 22,
  FLOOR(RAND()*35), FLOOR(RAND()*15), FLOOR(RAND()*10),
  FLOOR(RAND()*5), FLOOR(RAND()*3), FLOOR(RAND()*12),
  FLOOR(RAND()*10), FLOOR(RAND()*5), FLOOR(RAND()*10),
  SEC_TO_TIME(1800 + FLOOR(RAND()*1200)),
  FLOOR(RAND()*6)
FROM players;

INSERT INTO statistics (
  playerId, matchId,
  totalPoints, fieldGoals, threePointers,
  steals, blocks, rebounds,
  assists, turnovers, freeThrows,
  totalPlayTime, fouls
)
SELECT
  id, 23,
  FLOOR(RAND()*35), FLOOR(RAND()*15), FLOOR(RAND()*10),
  FLOOR(RAND()*5), FLOOR(RAND()*3), FLOOR(RAND()*12),
  FLOOR(RAND()*10), FLOOR(RAND()*5), FLOOR(RAND()*10),
  SEC_TO_TIME(1800 + FLOOR(RAND()*1200)),
  FLOOR(RAND()*6)
FROM players;

INSERT INTO statistics (
  playerId, matchId,
  totalPoints, fieldGoals, threePointers,
  steals, blocks, rebounds,
  assists, turnovers, freeThrows,
  totalPlayTime, fouls
)
SELECT
  id, 24,
  FLOOR(RAND()*35), FLOOR(RAND()*15), FLOOR(RAND()*10),
  FLOOR(RAND()*5), FLOOR(RAND()*3), FLOOR(RAND()*12),
  FLOOR(RAND()*10), FLOOR(RAND()*5), FLOOR(RAND()*10),
  SEC_TO_TIME(1800 + FLOOR(RAND()*1200)),
  FLOOR(RAND()*6)
FROM players;



       