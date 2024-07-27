-- reset valid email before update


CREATE TRIGGER reset_valid_email_before_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = FALSE;
    END IF;
END