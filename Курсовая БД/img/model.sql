DROP SCHEMA IF EXISTS `RealEstateAgency`;
CREATE SCHEMA `RealEstateAgency`;
USE `RealEstateAgency` ;

DROP TABLE IF EXISTS `RealEstateAgency`.`Client`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Client` (
  `clientID` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `contact` VARCHAR(15) NOT NULL,
  `passport` VARCHAR(9) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`clientID`),
  UNIQUE INDEX `passport_UNIQUE` (`passport` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `contact_UNIQUE` (`contact` ASC) VISIBLE)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`PropertyOwner`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`PropertyOwner` (
  `pownerID` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `contact` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`pownerID`),
  UNIQUE INDEX `contact_UNIQUE` (`contact` ASC) VISIBLE)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Property`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Property` (
  `propertyID` INT NOT NULL AUTO_INCREMENT,
  `street` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `postalcode` VARCHAR(10) NOT NULL,
  `floornumber` INT NULL,
  `area` VARCHAR(10) DEFAULT 'm^2',
  `numberofrooms` INT NOT NULL,
  `type` VARCHAR(4) NOT NULL,
  `pownerID` INT NOT NULL,
  PRIMARY KEY (`propertyID`, `pownerID`),
  INDEX `prop-pow_idx` (`pownerID` ASC) VISIBLE,
  CONSTRAINT `prop-pow`
    FOREIGN KEY (`pownerID`)
    REFERENCES `RealEstateAgency`.`PropertyOwner` (`pownerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Agency`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Agency` (
  `agencyID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `areaserver` VARCHAR(45) NOT NULL,
  `contact` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`agencyID`))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Agent`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Agent` (
  `agentID` INT NOT NULL AUTO_INCREMENT,
  `agencyID` INT NOT NULL,
  `clientID` INT NOT NULL,
  PRIMARY KEY (`agentID`, `agencyID`, `clientID`),
  INDEX `agent-cl_idx` (`clientID` ASC) VISIBLE,
  INDEX `agent-agency_idx` (`agencyID` ASC) VISIBLE,
  CONSTRAINT `agent-agency`
    FOREIGN KEY (`agencyID`)
    REFERENCES `RealEstateAgency`.`Agency` (`agencyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `agent-cl`
    FOREIGN KEY (`clientID`)
    REFERENCES `RealEstateAgency`.`Client` (`clientID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Listing`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Listing` (
  `listingID` INT NOT NULL AUTO_INCREMENT,
  `agentID` INT NOT NULL,
  `clientid` INT NOT NULL,
  `propertyID` INT NOT NULL,
  `listdate` DATETIME NOT NULL,
  `listprice` FLOAT NOT NULL,
  `url` VARCHAR(225) NOT NULL,
  `open` TINYINT DEFAULT TRUE,
  PRIMARY KEY (`listingID`, `agentID`, `propertyID`, `clientid`),
  INDEX `list-agent_idx` (`agentID` ASC) VISIBLE,
  INDEX `list-cl_idx` (`clientid` ASC) VISIBLE,
  INDEX `list-prop_idx` (`propertyID` ASC) VISIBLE,
  CONSTRAINT `list-agent`
    FOREIGN KEY (`agentID`)
    REFERENCES `RealEstateAgency`.`Agent` (`agentID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `list-cl`
    FOREIGN KEY (`clientid`)
    REFERENCES `RealEstateAgency`.`Client` (`clientID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `list-prop`
    FOREIGN KEY (`propertyID`)
    REFERENCES `RealEstateAgency`.`Property` (`propertyID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Offer`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Offer` (
  `offerID` INT NOT NULL AUTO_INCREMENT,
  `pownerID` INT NOT NULL,
  `listingID` INT NOT NULL,
  `validfrom` DATE NOT NULL,
  `validuntil` DATE NOT NULL,
  `price` FLOAT NOT NULL,
  `pricecurrency` VARCHAR(3) NOT NULL,
  `note` VARCHAR(225) NOT NULL,
  `accepted` TINYINT DEFAULT FALSE,
  PRIMARY KEY (`offerID`, `listingID`, `pownerID`),
  INDEX `off-pow_idx` (`pownerID` ASC) VISIBLE,
  INDEX `off-list_idx` (`listingID` ASC) VISIBLE,
  CONSTRAINT `off-pow`
    FOREIGN KEY (`pownerID`)
    REFERENCES `RealEstateAgency`.`PropertyOwner` (`pownerID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `off-list`
    FOREIGN KEY (`listingID`)
    REFERENCES `RealEstateAgency`.`Listing` (`listingID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Inquiry`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Inquiry` (
  `inquiryID` INT NOT NULL AUTO_INCREMENT,
  `propertyID` INT NOT NULL,
  `clientID` INT NOT NULL,
  PRIMARY KEY (`inquiryID`, `clientID`, `propertyID`),
  INDEX `in-prop_idx` (`propertyID` ASC) VISIBLE,
  INDEX `in-cl_idx` (`clientID` ASC) VISIBLE,
  CONSTRAINT `in-prop`
    FOREIGN KEY (`propertyID`)
    REFERENCES `RealEstateAgency`.`Property` (`propertyID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `in-cl`
    FOREIGN KEY (`clientID`)
    REFERENCES `RealEstateAgency`.`Client` (`clientID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Contract`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Contract` (
  `contractID` INT NOT NULL AUTO_INCREMENT,
  `pownerID` INT NOT NULL,
  `listingID` INT NOT NULL,
  `tax` FLOAT NOT NULL,
  PRIMARY KEY (`contractID`, `listingID`, `pownerID`),
  INDEX `con-pow_idx` (`pownerID` ASC) VISIBLE,
  INDEX `con-list_idx` (`listingID` ASC) VISIBLE,
  CONSTRAINT `con-pow`
    FOREIGN KEY (`pownerID`)
    REFERENCES `RealEstateAgency`.`PropertyOwner` (`pownerID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `con-list`
    FOREIGN KEY (`listingID`)
    REFERENCES `RealEstateAgency`.`Listing` (`listingID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Rent`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Rent` (
  `rentID` INT NOT NULL AUTO_INCREMENT,
  `contractID` INT NOT NULL,
  `validfrom` DATE NOT NULL,
  `validuntil` DATE NOT NULL,
  `monthlyprice` FLOAT NOT NULL,
  PRIMARY KEY (`rentID`, `contractID`),
  INDEX `rent-con_idx` (`contractID` ASC) VISIBLE,
  CONSTRAINT `rent-con`
    FOREIGN KEY (`contractID`)
    REFERENCES `RealEstateAgency`.`Contract` (`contractID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;
DROP FUN
DELIMITER $$


USE RealEstateAgency;

DELIMITER $$
CREATE FUNCTION dates(date1 DATETIME, date2 DATETIME)
RETURNS INT DETERMINISTIC
BEGIN
	RETURN YEAR(date2) - YEAR(date1) + (DATE_FORMAT(date2, '%m%d') > DATE_FORMAT(date1, '%m%d'));
END$$

CREATE TRIGGER add_email BEFORE INSERT ON Client
		FOR EACH ROW
        BEGIN
        IF NOT NEW.email NOT LIKE '[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$' THEN
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
        IF dates(NEW.validfrom, NEW.validuntil) <= 0 THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Incorrect data...';
		END IF;
END $$

CREATE TRIGGER add_valid_r_UP BEFORE UPDATE ON Rent
		FOR EACH ROW
        BEGIN
        IF dates(NEW.validfrom, NEW.validuntil) <= 0 THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Incorrect data...';
		END IF;
END $$

CREATE TRIGGER add_valid_O_UP AFTER UPDATE ON Offer
		FOR EACH ROW
        BEGIN
        DECLARE id INT;
        SELECT propertyID INTO id FROM Listing WHERE listingID = NEW.listingID;
        IF NEW.accepted = TRUE THEN
			DELETE FROM Property WHERE propertyID=id;
		END IF;
END $$

CREATE TRIGGER add_valid_L_UP AFTER UPDATE ON Listing
		FOR EACH ROW
        BEGIN
        IF NEW.open = TRUE THEN
			DELETE FROM Listing WHERE (propertyID=NEW.propertyID AND listingID=NEW.listingID);
		END IF;
END $$
DELIMITER ;

ALTER TABLE Client ADD CONSTRAINT c_clname CHECK ((firstname NOT LIKE '%[^A-Z]%') AND (lastname NOT LIKE '%[^A-Z]%'));
ALTER TABLE PropertyOwner ADD CONSTRAINT c_powname CHECK ((firstname NOT LIKE '%[^A-Z]%') AND (lastname NOT LIKE '%[^A-Z]%'));
ALTER TABLE Client ADD CONSTRAINT c_clpas CHECK ((passport NOT LIKE '%[^0-9]%') AND (LENGTH(passport)=9));
ALTER TABLE Client ADD CONSTRAINT c_clnum CHECK (contact NOT LIKE '%[^0-9+]%');
ALTER TABLE PropertyOwner ADD CONSTRAINT c_pownum CHECK (contact NOT LIKE '%[^0-9+]%');
ALTER TABLE Offer ADD CONSTRAINT c_prcur CHECK (pricecurrency NOT LIKE '%[^A-Z]%');
ALTER TABLE Property ADD CONSTRAINT c_type CHECK ((type = 'sale') OR(type = 'rent'));







