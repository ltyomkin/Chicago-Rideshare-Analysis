-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema trips_snowflake
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema trips_snowflake
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `trips_snowflake` DEFAULT CHARACTER SET utf8 ;
USE `trips_snowflake` ;

-- -----------------------------------------------------
-- Table `trips_snowflake`.`dim_time`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trips_snowflake`.`dim_time` (
  `timestamp_id` TIMESTAMP NOT NULL,
  `time` TIME NULL,
  `date` DATE NULL,
  `month` VARCHAR(10) NULL,
  `year` YEAR NULL,
  `weekday` VARCHAR(10) NULL,
  PRIMARY KEY (`timestamp_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `trips_snowflake`.`dim_base_region`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trips_snowflake`.`dim_base_region` (
  `base_region_id` INT(3) NOT NULL,
  `region_name` VARCHAR(45) NULL,
  `latitude` FLOAT NULL,
  `longitude` FLOAT NULL,
  PRIMARY KEY (`base_region_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `trips_snowflake`.`dim_trip_region`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trips_snowflake`.`dim_trip_region` (
  `trip_region_id` INT(5) NULL,
  `base_region_id` INT(3) NULL,
  `trip_centroids` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`trip_centroids`),
  INDEX `base_region_id_idx` (`base_region_id` ASC),
  CONSTRAINT `base_region_id`
    FOREIGN KEY (`base_region_id`)
    REFERENCES `trips_snowflake`.`dim_base_region` (`base_region_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `trips_snowflake`.`trips`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trips_snowflake`.`trips` (
  `Index` INT NULL,
  `trip_id` VARCHAR(45) NOT NULL,
  `ride_type_id` INT(2) NOT NULL,
  `start_timestamp_id` TIMESTAMP NOT NULL,
  `end_timestamp_id` TIMESTAMP NOT NULL,
  `duration_seconds` FLOAT NULL,
  `miles` FLOAT NULL,
  `fare` FLOAT NULL,
  `tip` FLOAT NULL,
  `tolls` FLOAT NULL,
  `extra_charges` FLOAT NULL,
  `trip_total` FLOAT NULL,
  `payment_type` VARCHAR(45) NULL,
  `pickup_centroid_location` VARCHAR(45) NULL,
  `dropoff_centroid_location` VARCHAR(45) NULL,
  PRIMARY KEY (`trip_id`),
  INDEX `start_timestamp_id_idx` (`start_timestamp_id` ASC),
  INDEX `end_timestamp_id_idx` (`end_timestamp_id` ASC),
  INDEX `pickup_centroid_location_idx` (`pickup_centroid_location` ASC),
  INDEX `dropoff_centroid_location_idx` (`dropoff_centroid_location` ASC),
  CONSTRAINT `start_timestamp_id`
    FOREIGN KEY (`start_timestamp_id`)
    REFERENCES `trips_snowflake`.`dim_time` (`timestamp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `end_timestamp_id`
    FOREIGN KEY (`end_timestamp_id`)
    REFERENCES `trips_snowflake`.`dim_time` (`timestamp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `pickup_centroid_location`
    FOREIGN KEY (`pickup_centroid_location`)
    REFERENCES `trips_snowflake`.`dim_trip_region` (`trip_centroids`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `dropoff_centroid_location`
    FOREIGN KEY (`dropoff_centroid_location`)
    REFERENCES `trips_snowflake`.`dim_trip_region` (`trip_centroids`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `trips_snowflake`.`dim_traffic`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trips_snowflake`.`dim_traffic` (
  `traffic_id` INT(10) NOT NULL,
  `region_id` INT(3) NOT NULL,
  `timestamp_id` TIMESTAMP NOT NULL,
  `speed` FLOAT NULL,
  `speed_category` VARCHAR(45) NULL,
  `bus_count` INT NULL,
  `gps_pings` INT NULL,
  PRIMARY KEY (`traffic_id`),
  INDEX `region_id_idx` (`region_id` ASC),
  INDEX `timestamp_id_idx` (`timestamp_id` ASC),
  CONSTRAINT `region_id`
    FOREIGN KEY (`region_id`)
    REFERENCES `trips_snowflake`.`dim_base_region` (`base_region_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `timestamp_id`
    FOREIGN KEY (`timestamp_id`)
    REFERENCES `trips_snowflake`.`dim_time` (`timestamp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
