# SQL Manager 2005 Lite for MySQL 3.7.7.1
# ---------------------------------------
# Host     : localhost
# Port     : 3306
# Database : dbchatbotclinicsys


SET FOREIGN_KEY_CHECKS=0;

CREATE DATABASE `dbchatbotclinicsys`
    CHARACTER SET 'latin1'
    COLLATE 'latin1_swedish_ci';

USE `dbchatbotclinicsys`;

#
# Structure for the `tblpatient` table : 
#

CREATE TABLE `tblpatient` (
  `Patient_ID` int(11) NOT NULL AUTO_INCREMENT,
  `PatientCode` varchar(100) NOT NULL,
  `PatientName` varchar(100) NOT NULL,
  `PatientLastName` varchar(100) NOT NULL,
  `PatientUserName` varchar(100) NOT NULL,
  `PatientPassword` varchar(100) NOT NULL,
  `PatientEmail` varchar(100) NOT NULL,
  `PatientNo` varchar(100) NOT NULL,
  PRIMARY KEY (`Patient_ID`),
  UNIQUE KEY `PatientCode` (`PatientCode`),
  UNIQUE KEY `PatientNo` (`PatientNo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

