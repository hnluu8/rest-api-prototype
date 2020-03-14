SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `community`;
CREATE SCHEMA IF NOT EXISTS `community` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `community`;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `community`.`user`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `community`.`user`;
CREATE TABLE IF NOT EXISTS `community`.`user` (
  `id`            INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `username`      VARCHAR(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name`          VARCHAR(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_date`  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_idx` (`username` ASC)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `community`.`question`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `community`.`question`;
CREATE TABLE IF NOT EXISTS `community`.`question` (
  `id`            INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `asker_id`      INT(11) UNSIGNED NOT NULL,
  `title`         VARCHAR(1000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_date`  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `user_idx` (`asker_id`),
  FOREIGN KEY (`asker_id`)
    REFERENCES `community`.`user` (`id`)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `community`.`response`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `community`.`response`;
CREATE TABLE IF NOT EXISTS `community`.`response` (
  `id`            INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `question_id`   INT(11) UNSIGNED NOT NULL,
  `responder_id`  INT(11) UNSIGNED NOT NULL,
  `text`          TEXT COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_date`  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX question_idx (`question_id`),
  INDEX responder_idx (`responder_id`),
  FOREIGN KEY (`question_id`)
    REFERENCES `community`.`question` (`id`)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY (`responder_id`)
    REFERENCES `community`.`user` (`id`)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


-- ---------------------------------------------------------------------------------------------------------------------
-- Table `community`.`questionbookmark`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `community`.`questionbookmark`;
CREATE TABLE IF NOT EXISTS `community`.`questionbookmark` (
  `id`            INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id`       INT(11) UNSIGNED NOT NULL,
  `question_id`   INT(11) UNSIGNED NOT NULL,
  `created_date`  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX user_question_idx (`user_id`, `question_id`),
  FOREIGN KEY (`user_id`)
    REFERENCES `community`.`user` (`id`)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY (`question_id`)
    REFERENCES `community`.`question` (`id`)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


-- ---------------------------------------------------------------------------------------------------------------------
-- Table `community`.`responsebookmark`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `community`.`responsebookmark`;
CREATE TABLE IF NOT EXISTS `community`.`responsebookmark` (
  `id`            INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id`       INT(11) UNSIGNED NOT NULL,
  `response_id`   INT(11) UNSIGNED NOT NULL,
  `created_date`  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX user_response_idx (`user_id`, `response_id`),
  FOREIGN KEY (`user_id`)
    REFERENCES `community`.`user` (`id`)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY (`response_id`)
    REFERENCES `community`.`response` (`id`)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
