USE dunkDetector;

-- Persona 1:
-- 1) As a coach, I want to keep track of my players’ game performance and other key statistics over the
-- season to identify trends and improvement areas.
SELECT P.firstname, P.lastname, S.*
FROM coaches C
JOIN teams T ON C.Id = T.CoachId
JOIN players P ON P.teamId = C.teamId
JOIN statistics S ON S.playerId = P.id;

-- 2) As a coach, I want to compare my players’ statistics with potential recruiters so I can make informed,
-- data-driven decisions about scouting and team development.
SELECT
    P.firstname AS player_firstname,
    P.lastname AS player_lastname,
    S.*,  -- Selecting all statistics for the current player
    R.firstname AS recruit_firstname,
    R.lastname AS recruit_lastname,
    SR.*  -- Selecting all statistics for the recruit
FROM coaches C
JOIN teams T ON C.id = T.coachId
JOIN players P ON P.teamId = T.id
JOIN statistics S ON P.id = S.playerId
LEFT JOIN players R ON R.id = @scouted_player_id
LEFT JOIN statistics SR ON SR.playerId = R.id;

-- 3) As a coach, I would like to view detailed scouting reports of my upcoming opponents so that
-- I can develop strategies tailored to their strengths and weaknesses.
SELECT
    opp_P.firstname AS opponent_firstname,
    opp_P.lastname AS opponent_lastname,
    sr.content AS scouting_report
FROM coaches C
JOIN teams T ON C.teamId = T.id
JOIN matches M ON (M.homeTeamId = T.id OR M.awayTeamId = T.id)
JOIN players opp_P ON (
    (M.homeTeamId = T.id AND opp_P.teamId = M.awayTeamId) OR
    (M.awayTeamId = T.id AND opp_P.teamId = M.homeTeamId)
)
JOIN scout_reports sr ON sr.playerId = opp_P.id
WHERE M.date > CURDATE()  -- Filter for future games
ORDER BY M.date;

-- 4) As a coach, I want to generate and export the scouting reports in a printable and legible format
-- so that I can share them with my coaching staff during meetings
SELECT 
    SR.reportDate, 
    SR.content, 
    SR.playerId
FROM scout_reports SR
ORDER BY SR.reportDate;

-- 5) As a coach, I want to log my own scouting notes on individual players. This way, I can keep track
-- of my qualitative evaluations and supplement the statistical data.
INSERT INTO reports (authorId, reportDate, content)
VALUES (4, NOW(), 'Strong tactical awareness.');

-- 6) As a coach, I want to be able to filter and search for players based on specific attributes so that
-- I can rapidly find athletes who fit my team’s needs. For example, I may want to identify players who
-- have made the most three-pointers across all matches, allowing me to prioritize sharpshooters for my
-- team's offensive strategy.
SELECT
    p.id,
    p.firstName,
    p.lastName,
    p.position,
    SUM(s.threePointers) AS total_three_pointers,
    COUNT(s.matchId) AS total_matches
FROM players p
JOIN statistics s ON p.id = s.playerId
GROUP BY p.firstName, p.id, p.lastName, p.position
HAVING total_matches > 1
ORDER BY total_three_pointers DESC;

-- Persona 2:
-- 1) As a data analyst, I need to filter player statistics based on minutes played
-- versus total season stats so that I can avoid misleading conclusions from small sample sizes.
SELECT
  	P.firstname,
    P.lastname,
    S.*
FROM players P
JOIN statistics S ON P.id = S.playerId
JOIN matches m ON S.matchId = m.id
WHERE S.totalPlayTime >= '00:30:00'  -- Minimum minutes played in a single game, adjust this as needed
ORDER BY m.date DESC;

-- 2) As a data analyst, I want to compare two players side by side using advanced visualizations so that
-- I can quickly assess their strengths and weaknesses.
SELECT
    P1.firstname AS player1_firstname,
    P1.lastname AS player1_lastname,
    S1.totalPoints AS player1_points,
    S1.threePointers AS player1_three_pointers,
    P2.firstname AS player2_firstname,
    P2.lastname AS player2_lastname,
    S2.totalPoints AS player2_points,
    S2.threePointers AS player2_three_pointers,
    m.date AS match_date
FROM statistics S1
JOIN players P1 ON P1.id = S1.playerId
JOIN statistics S2 ON S1.matchId = S2.matchId AND S1.playerId != S2.playerId
JOIN players P2 ON P2.id = S2.playerId
JOIN matches m ON S1.matchId = m.id
WHERE (P1.id = @player1_id AND P2.id = @player2_id) OR (P1.id = @player2_id AND P2.id = @player1_id)
ORDER BY m.date DESC;

-- 3) As a data analyst, I need a dashboard that summarizes key metrics per game
-- so that I can make data-driven recommendations to my team’s decision-makers.
SELECT
    p.id AS player_id,
    p.firstname,
    p.lastname,
    COUNT(DISTINCT s.matchId) AS games_played,
    SUM(s.totalPoints) / COUNT(DISTINCT s.matchId) AS points_per_game,
    SUM(s.assists) / COUNT(DISTINCT s.matchId) AS assists_per_game,
    SUM(s.rebounds) / COUNT(DISTINCT s.matchId) AS rebounds_per_game,
    SUM(s.steals) / COUNT(DISTINCT s.matchId) AS steals_per_game,
    SUM(s.blocks) / COUNT(DISTINCT s.matchId) AS blocks_per_game,
    SUM(s.turnovers) / COUNT(DISTINCT s.matchId) AS turnovers_per_game,
    SUM(s.fouls) / COUNT(DISTINCT s.matchId) AS fouls_per_game,
    SUM(s.fieldGoals) / NULLIF(SUM(s.totalPoints), 0) AS fg_percentage,
    SUM(s.threePointers) / NULLIF(SUM(s.fieldGoals), 0) AS three_pt_percentage,
    SUM(s.freeThrows) / NULLIF(SUM(s.totalPoints), 0) AS ft_percentage,
    SEC_TO_TIME(SUM(TIME_TO_SEC(s.totalPlayTime)) / COUNT(DISTINCT s.matchId)) AS avg_play_time
FROM statistics s
JOIN players p ON s.playerId = p.id
GROUP BY p.id, p.firstname, p.lastname
ORDER BY points_per_game DESC;

-- 4) As a data analyst, I want to access player contract details and agent information so that I
-- can evaluate potential signings from both performance and salary cap perspectives.
SELECT P.firstname, P.lastname, A.*
	FROM players P JOIN agents A ON P.agentId = A.id

-- 5) As a data analyst, I need a feature that suggests statistically similar players based on
-- advanced metrics so that I can identify underrated talents or trade targets.
SELECT 
    P.firstname, 
    P.lastname, 
    S.*
FROM players P
JOIN statistics S ON P.id = S.playerId
ORDER BY P.lastname, P.firstname;

-- 6) As a data analyst, I want to take notes and flag players directly in the platform so that I can
-- track insights without switching between different tools.
INSERT INTO reports (authorId, reportDate, content)
VALUES
(3, '2024-04-01', 'Player #1 showed excellent offensive skills.'),
(3, '2024-04-01', 'Player #2 struggles with consistency.');

-- Persona 3
-- 1)  As a General Manager, I need a dashboard summarizing top-tier college basketball prospects so
-- that I can focus on selecting the most promising players.
SELECT
    P.firstName AS player_firstname,
    P.lastName AS player_lastname,
    T.name AS team_name,
    T.city AS team_city,
    T.state AS team_state,
    T.country AS team_country,
    R.content AS report_content,
    R.reportDate
FROM reports R
JOIN users u ON R.authorId = u.id
JOIN scout_reports sr ON u.id = sr.authorId
JOIN players P ON sr.playerId = P.id
JOIN teams T ON T.id = P.teamId
WHERE T.isCollege = TRUE
ORDER BY R.reportDate DESC;

-- 2) As a General Manager, I need to access injury history reports so that I can assess
-- long-term durability of each player.
SELECT 
    I.*, 
    p.firstname, 
    p.lastname
FROM general_managers gm JOIN teams t on gm.teamId = t.id
JOIN players p ON p.teamId = t.id
JOIN injuries I ON I.id = p.injuryId;

-- 3) As a General Manager, I need to compare current prospects to past NBA players with
-- similar statistical profiles so that I can predict their potential success in the league.
-- (Assuming @player1_id is the current college player's ID and @player2_id is the past NBA player's ID)
SELECT
    P1.firstName AS current_player_firstname,
    P1.lastName AS current_player_lastname,
    S1.totalPoints AS current_player_totalPoints,
    S1.fieldGoals AS current_player_fieldGoals,
    S1.threePointers AS current_player_threePointers,
    S1.steals AS current_player_steals,
    S1.blocks AS current_player_blocks,
    S1.rebounds AS current_player_rebounds,
    S1.assists AS current_player_assists,
    S1.turnovers AS current_player_turnovers,
    S1.freeThrows AS current_player_freeThrows,
    S1.totalPlayTime AS current_player_totalPlayTime,
    S1.fouls AS current_player_fouls,

    P2.firstName AS nba_player_firstname,
    P2.lastName AS nba_player_lastname,
    S2.totalPoints AS nba_player_totalPoints,
    S2.fieldGoals AS nba_player_fieldGoals,
    S2.threePointers AS nba_player_threePointers,
    S2.steals AS nba_player_steals,
    S2.blocks AS nba_player_blocks,
    S2.rebounds AS nba_player_rebounds,
    S2.assists AS nba_player_assists,
    S2.turnovers AS nba_player_turnovers,
    S2.freeThrows AS nba_player_freeThrows,
    S2.totalPlayTime AS nba_player_totalPlayTime,
    S2.fouls AS nba_player_fouls

FROM players P1
JOIN statistics S1 ON P1.id = S1.playerId
JOIN players P2 ON P2.id = @player2_id
JOIN statistics S2 ON P2.id = S2.playerId

WHERE P1.id = @player1_id
ORDER BY S1.totalPoints DESC
LIMIT 10;

-- 4) As a General Manager, I need to filter players based on skill archetypes so that I can
-- focus on prospects who meet my team’s goals/needs.
SELECT
    P.firstName AS player_firstname,
    P.lastName AS player_lastname,
    T.name AS team_name,
    T.city AS team_city,
    T.state AS team_state,
    T.country AS team_country,
    R.content AS report_content,
    sr.content AS scout_report_content,
    R.reportDate
FROM reports R
JOIN users u ON R.authorId = u.id
JOIN scout_reports sr ON u.id = sr.authorId
JOIN players P on sr.playerId = P.id
JOIN teams T ON T.id = P.teamId
ORDER BY R.reportDate DESC;

-- 5) As a general manager, I need to generate customizable reports based on specific stats
-- (shooting efficiency, # of rebounds, etc) so that I can tailor my scouting approach to my team’s priorities.
SELECT 
    P.firstname, 
    P.lastname, 
    S.*
FROM players P
JOIN statistics S ON P.id = S.playerId
ORDER BY P.lastname, P.firstname;

-- 6) As a general manager, I need to see how players perform in high-pressure games (March Madness, conference
-- semis/finals) so that I can evaluate their ability to handle NBA-level intensity.
-- Assuming @start_date and @end_date are provided by the user
SELECT
    P.firstName AS player_firstname,
    P.lastName AS player_lastname,
    S.*,  -- All statistics for the player
    M.date AS game_date,       -- Date of the game
    M.location AS game_location,  -- Location of the game
    M.homeScore,               -- Home team score
    M.awayScore                -- Away team score
FROM players P
JOIN statistics S ON P.id = S.playerId
JOIN matches M ON S.matchId = M.id
WHERE M.date BETWEEN @start_date AND @end_date  -- Filter for games within the date range
ORDER BY M.date DESC;

-- 7) As a general manager, I need to have access to my data analysts reports on different players, so I can
-- make quick decisions on player recruitment.
-- Retrieve scout reports for players, excluding user information
SELECT
    P.firstName AS player_firstname,
    P.lastName AS player_lastname,
    SR.reportDate AS report_date,
    SR.content AS report_content
FROM scout_reports SR
JOIN players P ON SR.playerId = P.id
JOIN users U ON SR.authorId = U.id  -- Assuming there's a 'users' table and 'userId' column in scout_reports
WHERE U.role = 'Data Analyst'
ORDER BY SR.reportDate DESC;

-- 8) As a general manager, I need to have access to my coaches reports to see what he thinks the team is lacking,
-- or which players he isn’t fond of anymore.
SELECT
    P.firstName AS player_firstname,
    P.lastName AS player_lastname,
    SR.reportDate AS report_date,
    SR.content AS report_content
FROM scout_reports SR
JOIN players P ON SR.playerId = P.id
JOIN users U ON SR.authorId = U.id
WHERE U.role = 'Coach'
ORDER BY SR.reportDate DESC;

-- 9) As a general manager, I need to be able to generate a report that takes into
-- account both the data analysts’ reports and the coaches reports in order to make
-- good decisions about squad building.
SELECT
    P.firstName AS player_firstname,
    P.lastName AS player_lastname,
    SR.reportDate AS report_date,
    SR.content AS report_content
FROM scout_reports SR
JOIN players P ON SR.playerId = P.id
JOIN users U ON SR.authorId = U.id
WHERE U.role IN ('Data Analyst', 'Coach')
ORDER BY SR.reportDate DESC;

-- Persona 4

-- 1) As a system administrator, I need to implement batch update processes so I can
-- efficiently correct player statistics across different competitions (playoffs,
-- in-season tournaments, March Madness, etc.)
UPDATE statistics
SET steals = 5
WHERE playerId = 1 && matchId = 1;

-- 2)  As a system administrator, I need to develop a streamlined workflow for updating
-- player profiles so that all roster changes are correctly displayed in a timely manner.
UPDATE players
SET height = 250
WHERE firstName = 'James' && middleName = 'Frank' && lastName = 'Harden';

-- 3) As a system administrator, I need to establish automated data ingestion pipelines
-- so new games can be quickly added to the system.
INSERT INTO matches (homeTeamId, awayTeamId, date, time, location, homeScore, awayScore, finalScore)
VALUES (1, 2, '2025-04-01', '19:30:00', 'Chicago', 100, 95, '100-95');

-- 4) INSERT players (firstName, middleName, lastName, agentId, position, teamId, height,
-- weight, dob, injuryId)
INSERT players (firstName, middleName, lastName, agentId, position, teamId, height, weight, dob, injuryId)
VALUES ('Luka', NULL, 'Doncic', 1, 'Point Guard', 1, 198, 300, '1999-02-28', 3);

-- 5) As a system administrator, I need to implement data archiving protocols to remove outdated \
-- data and scouting reports.
DELETE FROM reports WHERE authorId = 1;
DELETE FROM scout_reports WHERE authorId = 1;

-- 6) As a system administrator, I need to develop a system that allows me to flag statistical
-- anomalies or data inconsistencies that can be marked for review and or potential removal.
UPDATE teams t
JOIN players p ON t.id = p.teamId
SET t.isProfessional = False
WHERE p.id = 1;

-- 7) As a data administrator, I need to ensure that I have a robust system that will remove
-- the data of players as they retire from the league and ensure it gets properly archived.
DELETE FROM players
WHERE firstName='James' && middleName='Frank' && lastName='Harden';