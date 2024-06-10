-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema users_and_animes
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `users_and_animes` ;

-- -----------------------------------------------------
-- Schema users_and_animes
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `users_and_animes` DEFAULT CHARACTER SET utf8 ;
USE `users_and_animes` ;

-- -----------------------------------------------------
-- Table `users_and_animes`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `users_and_animes`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `users_and_animes`.`animes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `users_and_animes`.`animes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `plot` TEXT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_animes_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_animes_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `users_and_animes`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `users_and_animes`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `users_and_animes`.`reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `anime_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `review_of_anime` TEXT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`, `anime_id`, `user_id`),
  INDEX `fk_animes_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_animes_has_users_animes1_idx` (`anime_id` ASC) VISIBLE,
  CONSTRAINT `fk_animes_has_users_animes1`
    FOREIGN KEY (`anime_id`)
    REFERENCES `users_and_animes`.`animes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_animes_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `users_and_animes`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
