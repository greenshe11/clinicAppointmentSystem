-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dbchatbotclinicsys
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tblappointment`
--

DROP TABLE IF EXISTS `tblappointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblappointment` (
  `Appointment_ID` int NOT NULL AUTO_INCREMENT,
  `Patient_ID` int NOT NULL,
  `Celendar_ID` int NOT NULL,
  `Smsnotif_ID` int NOT NULL,
  `Diagnosis_ID` int NOT NULL,
  `Appointment_Day` int NOT NULL,
  `Appointment_Month` int NOT NULL,
  `Appointment_Time` int NOT NULL,
  `Appointment_Year` int NOT NULL,
  PRIMARY KEY (`Appointment_ID`),
  UNIQUE KEY `PatientCode` (`Patient_ID`),
  UNIQUE KEY `Celendar_ID` (`Celendar_ID`),
  UNIQUE KEY `Smsnotif_ID` (`Smsnotif_ID`),
  UNIQUE KEY `Chatlog_ID` (`Diagnosis_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblappointment`
--

LOCK TABLES `tblappointment` WRITE;
/*!40000 ALTER TABLE `tblappointment` DISABLE KEYS */;
INSERT INTO `tblappointment` VALUES (2,1,1,1,1,12,100,11,2024);
/*!40000 ALTER TABLE `tblappointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbldiagnosis`
--

DROP TABLE IF EXISTS `tbldiagnosis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbldiagnosis` (
  `Diagnosis_ID` int NOT NULL AUTO_INCREMENT,
  `Patient_ID` int NOT NULL,
  `Diagnosis_Symptoms` varchar(100) NOT NULL,
  `Diagnosis_Pre` text NOT NULL,
  PRIMARY KEY (`Diagnosis_ID`),
  UNIQUE KEY `Patient_ID` (`Patient_ID`),
  CONSTRAINT `tbldiagnosis_Patient_ID_fk1` FOREIGN KEY (`Patient_ID`) REFERENCES `tblpatient` (`Patient_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbldiagnosis`
--

LOCK TABLES `tbldiagnosis` WRITE;
/*!40000 ALTER TABLE `tbldiagnosis` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbldiagnosis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblpatient`
--

DROP TABLE IF EXISTS `tblpatient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblpatient` (
  `Patient_ID` int NOT NULL AUTO_INCREMENT,
  `PatientCode` varchar(100) DEFAULT NULL,
  `PatientName` varchar(100) NOT NULL,
  `PatientLastName` varchar(100) NOT NULL,
  `PatientPassword` varchar(100) NOT NULL,
  `PatientEmail` varchar(100) NOT NULL,
  `PatientContactNo` varchar(100) NOT NULL,
  PRIMARY KEY (`Patient_ID`),
  UNIQUE KEY `PatientContactNo_UNIQUE` (`PatientContactNo`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblpatient`
--

LOCK TABLES `tblpatient` WRITE;
/*!40000 ALTER TABLE `tblpatient` DISABLE KEYS */;
INSERT INTO `tblpatient` VALUES (10,'P-10','Roan','Langreo','123','roan@email.com','096782'),(18,NULL,'asdas','asdad','$2b$12$JnJ6eUHuIAW3XKNzlLzMJeqMMO4gWXGRvewJxu1HbArrH/NegjIB2','reynalie23@yahoo.com','123123123'),(28,NULL,'asdas','asd','$2b$12$EbqPTX58BS25G7NE7l7/DOlXvXUg4jsN7XfoI/TZV.Ieyv86p1ynO','123@1231','1231231231'),(32,NULL,'asdas','asas','$2b$12$sB.CLyDZAT2U6WojANvvl.AGa9dclLYEYffzvS1cgCK3qeiAt5JJ.','as@as2','1231231231123'),(33,NULL,'asdasd','asdasd','$2b$12$NdAE7.6cJCTvSQ8GFsLVOOZBOLbs.ZLTtNVQMN6O/GHkwGilWZtLm','asas@asas','asas'),(34,NULL,'Eugene Dave','Tumagan','$2b$12$d5mXMin201bL8MFDb5xIt.cii21TWH2dOkQZFdF9XD8Ymt2wCKEOK','eugenetumagan02@gmail.com','09674688324');
/*!40000 ALTER TABLE `tblpatient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblsmsnotif`
--

DROP TABLE IF EXISTS `tblsmsnotif`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblsmsnotif` (
  `Smsnotif_ID` int NOT NULL AUTO_INCREMENT,
  `Patient_ID` int NOT NULL,
  `PatientContactNo` varchar(100) NOT NULL,
  `Smsnotif_Message` text,
  `Smsnotif_Date` datetime NOT NULL,
  PRIMARY KEY (`Smsnotif_ID`),
  UNIQUE KEY `PatientCode` (`Patient_ID`),
  UNIQUE KEY `PatientNo` (`PatientContactNo`),
  CONSTRAINT `tblsmsnotif_Patient_ID_fk_1` FOREIGN KEY (`Patient_ID`) REFERENCES `tblpatient` (`Patient_ID`) ON UPDATE CASCADE,
  CONSTRAINT `tblsmsnotif_PatientNo_fk_2` FOREIGN KEY (`PatientContactNo`) REFERENCES `tblpatient` (`PatientContactNo`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblsmsnotif`
--

LOCK TABLES `tblsmsnotif` WRITE;
/*!40000 ALTER TABLE `tblsmsnotif` DISABLE KEYS */;
/*!40000 ALTER TABLE `tblsmsnotif` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-30 11:30:56
