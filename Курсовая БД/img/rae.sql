DROP SCHEMA IF EXISTS `RealEstateAgency`;
CREATE SCHEMA IF NOT EXISTS `RealEstateAgency`;
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
  UNIQUE INDEX `passport_UNIQUE` (`passport` ASC) VISIBLE)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`PropertyOwner`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`PropertyOwner` (
  `pownerID` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `contact` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`pownerID`),
  UNIQUE INDEX `firstname_UNIQUE` (`firstname` ASC) VISIBLE,
  UNIQUE INDEX `lastname_UNIQUE` (`lastname` ASC) VISIBLE,
  UNIQUE INDEX `contact_UNIQUE` (`contact` ASC) VISIBLE)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Property`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Property` (
  `propertyID` INT NOT NULL AUTO_INCREMENT,
  `street` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `postalcode` VARCHAR(10) NOT NULL,
  `floornumber` INT NULL,
  `area` VARCHAR(10) NOT NULL,
  `numberofrooms` INT NOT NULL,
  `type` VARCHAR(4) NOT NULL,
  `pownerID` INT NOT NULL,
  PRIMARY KEY (`propertyID`, `pownerID`),
  UNIQUE INDEX `type_UNIQUE` (`type` ASC) VISIBLE,
  UNIQUE INDEX `area_UNIQUE` (`area` ASC) VISIBLE,
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
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
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
  UNIQUE INDEX `open_UNIQUE` (`open` ASC) VISIBLE,
  UNIQUE INDEX `listdate_UNIQUE` (`listdate` ASC) VISIBLE,
  UNIQUE INDEX `url_UNIQUE` (`url` ASC) VISIBLE,
  INDEX `list-agent_idx` (`agentID` ASC) VISIBLE,
  INDEX `list-cl_idx` (`clientid` ASC) VISIBLE,
  INDEX `list-prop_idx` (`propertyID` ASC) VISIBLE,
  CONSTRAINT `list-agent`
    FOREIGN KEY (`agentID`)
    REFERENCES `RealEstateAgency`.`Agent` (`agentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `list-cl`
    FOREIGN KEY (`clientid`)
    REFERENCES `RealEstateAgency`.`Client` (`clientID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `list-prop`
    FOREIGN KEY (`propertyID`)
    REFERENCES `RealEstateAgency`.`Property` (`propertyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Offer`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Offer` (
  `offerID` INT NOT NULL AUTO_INCREMENT,
  `pownerID` INT NOT NULL,
  `listingID` INT NOT NULL,
  `validfrom` DATETIME NOT NULL,
  `validuntil` DATETIME NOT NULL,
  `price` FLOAT NOT NULL,
  `pricecurrency` VARCHAR(3) NOT NULL,
  `note` VARCHAR(225) NOT NULL,
  `accepted` TINYINT DEFAULT FALSE,
  PRIMARY KEY (`offerID`, `listingID`, `pownerID`),
  UNIQUE INDEX `validfrom_UNIQUE` (`validfrom` ASC) VISIBLE,
  UNIQUE INDEX `validuntil_UNIQUE` (`validuntil` ASC) VISIBLE,
  UNIQUE INDEX `pricecurrency_UNIQUE` (`pricecurrency` ASC) VISIBLE,
  INDEX `off-pow_idx` (`pownerID` ASC) VISIBLE,
  INDEX `off-list_idx` (`listingID` ASC) VISIBLE,
  CONSTRAINT `off-pow`
    FOREIGN KEY (`pownerID`)
    REFERENCES `RealEstateAgency`.`PropertyOwner` (`pownerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `off-list`
    FOREIGN KEY (`listingID`)
    REFERENCES `RealEstateAgency`.`Listing` (`listingID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
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
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `in-cl`
    FOREIGN KEY (`clientID`)
    REFERENCES `RealEstateAgency`.`Client` (`clientID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
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
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `con-list`
    FOREIGN KEY (`listingID`)
    REFERENCES `RealEstateAgency`.`Listing` (`listingID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `RealEstateAgency`.`Rent`;
CREATE TABLE IF NOT EXISTS `RealEstateAgency`.`Rent` (
  `rentID` INT NOT NULL AUTO_INCREMENT,
  `contractID` INT NOT NULL,
  `validfrom` DATETIME NOT NULL,
  `validuntil` DATETIME NOT NULL,
  `monthlyprice` FLOAT NOT NULL,
  PRIMARY KEY (`rentID`, `contractID`),
  INDEX `rent-con_idx` (`contractID` ASC) VISIBLE,
  UNIQUE INDEX `validfrom_UNIQUE` (`validfrom` ASC) VISIBLE,
  UNIQUE INDEX `validuntil_UNIQUE` (`validuntil` ASC) VISIBLE,
  CONSTRAINT `rent-con`
    FOREIGN KEY (`contractID`)
    REFERENCES `RealEstateAgency`.`Contract` (`contractID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


