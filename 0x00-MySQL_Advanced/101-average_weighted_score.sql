-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE userId INT;
    DECLARE userCursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    OPEN userCursor;
    user_loop: LOOP
        FETCH userCursor INTO userId;
        IF done THEN
            LEAVE user_loop;
        END IF;
        
        UPDATE users u
        SET u.average_score = (
            SELECT IFNULL(SUM(c.score * p.weight) / SUM(p.weight), 0)
            FROM corrections c
            JOIN projects p ON c.project_id = p.id
            WHERE c.user_id = userId
        )
        WHERE u.id = userId;
    END LOOP;
    CLOSE userCursor;
END

DELIMITER ;