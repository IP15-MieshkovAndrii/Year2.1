USE RealEstateAgency;

DELIMITER $$
CREATE FUNCTION dates(date1 DATETIME, date2 DATETIME)
RETURNS INT DETERMINISTIC
BEGIN
	RETURN YEAR(date2) - YEAR(date1) - (DATE_FORMAT(date2, '%m%d') < DATE_FORMAT(date1, '%m%d'));
END$$

CREATE TRIGGER add_email BEFORE INSERT ON Client
		FOR EACH ROW
        BEGIN
        IF NEW.email NOT LIKE '[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$' THEN
			SET NEW.email = NULL;
		END IF;
END $$

CREATE TRIGGER add_area BEFORE INSERT ON Property
		FOR EACH ROW
        BEGIN
        IF NEW.area NOT LIKE '%[^0-9]%' THEN
			SET NEW.area = CONCAT(NEW.area,'m^2');
		END IF;
END $$

CREATE TRIGGER add_valid_of BEFORE INSERT ON Offer
		FOR EACH ROW
        BEGIN
        IF dates(NEW.validfrom, NEW.validuntil) < 0 THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Incorrect data...';
		END IF;
END $$

CREATE TRIGGER add_valid_r BEFORE INSERT ON Rent
		FOR EACH ROW
        BEGIN
        IF dates(NEW.validfrom, NEW.validuntil) < 0 THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Incorrect data...';
		END IF;
END $$

CREATE TRIGGER add_email_UP BEFORE UPDATE ON Client
		FOR EACH ROW
        BEGIN
        IF NEW.email NOT LIKE '[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$' THEN
			SET NEW.email = NULL;
		END IF;
END $$

CREATE TRIGGER add_area_UP BEFORE UPDATE ON Property
		FOR EACH ROW
        BEGIN
        IF NEW.area NOT LIKE '%[^0-9]%' THEN
			SET NEW.area = CONCAT(NEW.area,'m^2');
		END IF;
END $$

CREATE TRIGGER add_valid_of_UP BEFORE UPDATE ON Offer
		FOR EACH ROW
        BEGIN
        IF dates(NEW.validfrom, NEW.validuntil) < 0 THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Incorrect data...';
		END IF;
END $$

CREATE TRIGGER add_valid_r_UP BEFORE UPDATE ON Rent
		FOR EACH ROW
        BEGIN
        IF dates(NEW.validfrom, NEW.validuntil) < 0 THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Incorrect data...';
		END IF;
END $$
DELIMITER ;

ALTER TABLE Client ADD CONSTRAINT c_clname CHECK ((firstname NOT LIKE '%[^A-Z]%') AND (lastname NOT LIKE '%[^A-Z]%'));
ALTER TABLE PropertyOwner ADD CONSTRAINT c_powname CHECK ((firstname NOT LIKE '%[^A-Z]%') AND (lastname NOT LIKE '%[^A-Z]%'));
ALTER TABLE Client ADD CONSTRAINT c_clpas CHECK ((passport NOT LIKE '%[^0-9]%') AND (LENGTH(passport)=9));
ALTER TABLE Client ADD CONSTRAINT c_clnum CHECK (contact NOT LIKE '%[^0-9+]%');
ALTER TABLE PropertyOwner ADD CONSTRAINT c_pownum CHECK (contact NOT LIKE '%[^0-9+]%');
ALTER TABLE Offer ADD CONSTRAINT c_prcur CHECK (pricecurrency NOT LIKE '%[^A-Z]%');







