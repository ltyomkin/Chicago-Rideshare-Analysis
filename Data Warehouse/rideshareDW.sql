-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`dim_rideshare_availability`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`dim_rideshare_availability` (
  `month_year_id` INT(4) NOT NULL,
  `drivers_available` VARCHAR(45) NULL,
  `drivers_active` INT(8) NULL,
  `drivers_multiple_tnps` INT(8) NULL,
  `vehicles_available` INT(10) NULL,
  `vehicles_with_trips` INT(10) NULL,
  `vehicles_multiple_tnps` INT(10) NULL,
  PRIMARY KEY (`month_year_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`dim_ride_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`dim_ride_type` (
  `ride_type_id` INT(2) NOT NULL,
  `ride_type` VARCHAR(45) NULL,
  PRIMARY KEY (`ride_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`dim_l_stations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`dim_l_stations` (
  `station_id` INT(3) NOT NULL,
  `station_name` VARCHAR(45) NULL,
  `line` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  PRIMARY KEY (`station_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`dim_bus_stops`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`dim_bus_stops` (
  `stop_id` INT(6) NOT NULL,
  `stop_name` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  PRIMARY KEY (`stop_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`dim_segment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`dim_segment` (
  `segment_id` INT(10) NOT NULL,
  `street` VARCHAR(45) NULL,
  `direction` VARCHAR(10) NULL,
  `from_street` VARCHAR(45) NULL,
  `to_street` VARCHAR(45) NULL,
  `length` FLOAT NULL,
  `street_heading` CHAR(10) NULL,
  `comments` VARCHAR(90) NULL,
  `bus_count` INT NULL,
  `start_latitude` FLOAT NULL,
  `start_longitude` FLOAT NULL,
  `end_latitude` FLOAT NULL,
  `end_longitude` FLOAT NULL,
  `start_location` VARCHAR(45) NULL,
  `end_location` VARCHAR(45) NULL,
  `station_id` INT(3) NULL,
  `stop_id` INT(6) NULL,
  PRIMARY KEY (`segment_id`),
  INDEX `station_id_idx` (`station_id` ASC) VISIBLE,
  INDEX `stop_id_idx` (`stop_id` ASC) VISIBLE,
  CONSTRAINT `station_id`
    FOREIGN KEY (`station_id`)
    REFERENCES `mydb`.`dim_l_stations` (`station_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `stop_id`
    FOREIGN KEY (`stop_id`)
    REFERENCES `mydb`.`dim_bus_stops` (`stop_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`dim_time`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`dim_time` (
  `timestamp_id` INT(20) NOT NULL,
  `time` TIME NULL,
  `date` DATE NULL,
  `month` VARCHAR(10) NULL,
  `year` YEAR NULL,
  `weekday` VARCHAR(10) NULL,
  `month_year_id` INT(4) NULL,
  PRIMARY KEY (`timestamp_id`),
  INDEX `month_year_id_idx` (`month_year_id` ASC) VISIBLE,
  CONSTRAINT `month_year_id`
    FOREIGN KEY (`month_year_id`)
    REFERENCES `mydb`.`dim_rideshare_availability` (`month_year_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`trips`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`trips` (
  `trip_id` INT(20) NOT NULL,
  `ride_type_id` INT(2) NOT NULL,
  `start_timestamp_id` INT(20) NOT NULL,
  `end_timestamp_id` INT(20) NOT NULL,
  `duration_seconds` INT NULL,
  `miles` DOUBLE NULL,
  `start_census_tract` BIGINT NULL,
  `end_census_tract` BIGINT NULL,
  `fare` DOUBLE NULL,
  `tip` DOUBLE NULL,
  `tolls` DOUBLE NULL,
  `extra_charges` DECIMAL NULL,
  `trip_total` DOUBLE NULL,
  `payment_type` SMALLINT NULL,
  `start_segment_id` INT(10) NULL,
  `end_segment_id` INT(10) NULL,
  PRIMARY KEY (`trip_id`),
  INDEX `ride_type_id_idx` (`ride_type_id` ASC) VISIBLE,
  INDEX `start_segment_id_idx` (`start_segment_id` ASC) VISIBLE,
  INDEX `end_segment_id_idx` (`end_segment_id` ASC) VISIBLE,
  INDEX `start_timestamp_id_idx` (`start_timestamp_id` ASC) VISIBLE,
  INDEX `end_timestamp_id_idx` (`end_timestamp_id` ASC) VISIBLE,
  CONSTRAINT `ride_type_id`
    FOREIGN KEY (`ride_type_id`)
    REFERENCES `mydb`.`dim_ride_type` (`ride_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `start_segment_id`
    FOREIGN KEY (`start_segment_id`)
    REFERENCES `mydb`.`dim_segment` (`segment_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `end_segment_id`
    FOREIGN KEY (`end_segment_id`)
    REFERENCES `mydb`.`dim_segment` (`segment_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `start_timestamp_id`
    FOREIGN KEY (`start_timestamp_id`)
    REFERENCES `mydb`.`dim_time` (`timestamp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `end_timestamp_id`
    FOREIGN KEY (`end_timestamp_id`)
    REFERENCES `mydb`.`dim_time` (`timestamp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`dim_traffic`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`dim_traffic` (
  `traffic_id` INT(12) NOT NULL,
  `segment_id` INT NOT NULL,
  `timestamp_id` INT(20) NOT NULL,
  `speed` INT NULL,
  `speed_category` VARCHAR(45) NULL,
  `comments` VARCHAR(90) NULL,
  `bus_count` INT NULL,
  `gps_pings` INT NULL,
  PRIMARY KEY (`traffic_id`),
  INDEX `segment_id_idx` (`segment_id` ASC) VISIBLE,
  INDEX `timestamp_id_idx` (`timestamp_id` ASC) VISIBLE,
  CONSTRAINT `segment_id`
    FOREIGN KEY (`segment_id`)
    REFERENCES `mydb`.`dim_segment` (`segment_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `timestamp_id`
    FOREIGN KEY (`timestamp_id`)
    REFERENCES `mydb`.`dim_time` (`timestamp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
