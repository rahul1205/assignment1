-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: assignment1b
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `assignment1b`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `assignment1b` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `assignment1b`;

--
-- Table structure for table `awardsandprizes`
--

DROP TABLE IF EXISTS `awardsandprizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `awardsandprizes` (
  `id` int(11) NOT NULL,
  `type_of_grant` varchar(200) DEFAULT NULL,
  `ResearchOffice_office_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`ResearchOffice_office_id`),
  KEY `fk_AwardsAndPrizes_ResearchOffices1_idx` (`ResearchOffice_office_id`),
  CONSTRAINT `fk_AwardsAndPrizes_ResearchOffices1` FOREIGN KEY (`ResearchOffice_office_id`) REFERENCES `researchoffice` (`office_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awardsandprizes`
--

LOCK TABLES `awardsandprizes` WRITE;
/*!40000 ALTER TABLE `awardsandprizes` DISABLE KEYS */;
INSERT INTO `awardsandprizes` VALUES (0,'Fellow of the Royal Society of Canada - Awards',1),(1,'NSERC John C. Polanyi Award',1),(2,'The Brockhouse Canada Prize for Interdisciplinary Research in Science and Engineering',1),(3,'The Gerhard Herzberg Canada Gold Medal for Science and Engineering',1),(4,'Royal Society of Canada, College of New Scholars, Artists and Scientists',1),(5,'Canadian Academy of Health Sciences (CAHS) Fellowship',1),(6,'Impact Awards - Gold Medal',1),(7,'Impact Awards - Insight Award',1),(8,'Impact Awards - Connection Award',1),(9,'Impact Awards - Partnership Award',1),(10,'Killam Research Fellowships',1),(11,'Discovery Awards',1),(12,'NSERC E.W.R. Steacie Memorial Fellowships',1),(13,'Killam Prizes',1),(14,'Chemical Institute of Canada Medal',1),(15,'Montreal Medal',1),(16,'The Prix Galien',1),(17,'Sloan Research Fellowships',1),(18,'Molson Prizes',1),(19,'Fellow of the Royal Society of Canada',1),(20,'Trudeau Fellowship',1),(21,'The Order of Canada',1);
/*!40000 ALTER TABLE `awardsandprizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campus`
--

DROP TABLE IF EXISTS `campus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campus` (
  `campus_id` int(11) NOT NULL,
  `campus_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`campus_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campus`
--

LOCK TABLES `campus` WRITE;
/*!40000 ALTER TABLE `campus` DISABLE KEYS */;
INSERT INTO `campus` VALUES (0,'studley'),(1,'sexton'),(2,'carleton'),(3,'truro');
/*!40000 ALTER TABLE `campus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `department_id` int(11) NOT NULL AUTO_INCREMENT,
  `department_name` varchar(100) DEFAULT NULL,
  `Faculty_faculty_id` int(11) NOT NULL,
  PRIMARY KEY (`department_id`),
  KEY `fk_Department_Faculty_idx` (`Faculty_faculty_id`),
  CONSTRAINT `fk_Department_Faculty` FOREIGN KEY (`Faculty_faculty_id`) REFERENCES `faculty` (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'Business and Social Sciences',0),(2,'Engineering',0),(3,'Plant, Food, and Environmental Sciences',0),(4,'Animal Science and Aquaculture',0),(5,'School of Architecture',1),(6,'School of Planning',1),(7,'Canadian Studies Program',2),(8,'Department of Classics',2),(9,'Department of English',2),(10,'Department of French',2),(11,'Gender and Women\'s Studies Program',2),(12,'Department of German',2),(13,'Department of History',2),(14,'Department of International Development Studies',2),(15,'Law, Justice and Society Program',2),(16,'Fountain School of Performing Arts',2),(17,'Department of Philosophy',2),(18,'Department of Political Science',2),(19,'Department of Russian Studies',2),(20,'Department of Sociology and Social Anthropology',2),(21,'Department of Spanish Latin American Studies',2),(22,'Civil and Resource Engineering',6),(23,'Electrical and Computer Engineering',6),(24,'Engineering Mathematics and Internetworking',6),(25,'Industrial Engineering',6),(26,'Mechanical Engineering',6),(27,'Process Engineering and Applied Science (PEAS)',6),(28,'School of Biomedical Engineering',6),(29,'School of Health and Human Performance',8),(30,'School of Health Administration',8),(31,'School of Health Sciences',8),(32,'School of Communication Sciences and Disorders',8),(33,'School of Nursing',8),(34,'School of Occupational Therapy',8),(35,'College of Pharmacy',8),(36,'School of Physiotherapy',8),(37,'School of Social Work',8),(38,'Rowe School of Business',10),(39,'School of Information Management',10),(40,'School of Public Administration',10),(41,'School for Resource and Environmental Studies',10),(42,'Department of Anesthesia, Pain Management and Peroperative Medicine',11),(43,'Department of Biochemistry and Molecular Biology',11),(44,'Department of Bioethics',11),(45,'School of Biomedical Engineering',11),(46,'Department of Community Health and Epidemiology',11),(47,'Department of Critical Care',11),(48,'Department of Diagnostic Radiology',11),(49,'Department of Emergency Medicine',11),(50,'Department of Family Medicine',11),(51,'Department of Medical Neuroscience',11),(52,'Department of Medicine',11),(53,'Department of Microbiology and Immunology',11),(54,'Department of Obstetrics and Gynaecology',11),(55,'Department of Ophthalmology and Visual Sciences',11),(56,'Department of Pathology',11),(57,'Department of Pediatrics',11),(58,'Department of Pharmacology',11),(59,'Department of Physiology and Biophysics',11),(60,'Department of Psychiatry',11),(61,'Department of Radiation Oncology',11),(62,'Department of Surgery',11),(63,'Department of Urology',11),(64,'Department of Biology',12),(65,'Department of Chemistry',12),(66,'Department of Earth Sciences',12),(67,'Department of Economics',12),(68,'Environmental Science Program',12),(69,'Marine Affairs Program',12),(70,'Department of Mathematics and Statistics',12),(71,'Department of Oceanography',12),(72,'Department of Physics and Atmospheric Science',12),(73,'Department of Psychology and Neuroscience',12);
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `externalfunding`
--

DROP TABLE IF EXISTS `externalfunding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `externalfunding` (
  `id` int(11) NOT NULL,
  `type_of_grant` varchar(200) DEFAULT NULL,
  `ResearchOffice_office_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`ResearchOffice_office_id`),
  KEY `fk_ExternalFunding_ResearchOffices1_idx` (`ResearchOffice_office_id`),
  CONSTRAINT `fk_ExternalFunding_ResearchOffices1` FOREIGN KEY (`ResearchOffice_office_id`) REFERENCES `researchoffice` (`office_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `externalfunding`
--

LOCK TABLES `externalfunding` WRITE;
/*!40000 ALTER TABLE `externalfunding` DISABLE KEYS */;
INSERT INTO `externalfunding` VALUES (0,'federal funding',1),(1,'provincial funding',1),(2,'not-for-profit funding',1),(3,'international funding',1),(4,'industry funding',1);
/*!40000 ALTER TABLE `externalfunding` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilitysubtype`
--

DROP TABLE IF EXISTS `facilitysubtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilitysubtype` (
  `id` int(11) NOT NULL,
  `facility_subtype` varchar(45) DEFAULT NULL,
  `FacilityType_facility_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_FacilitySubType_FacilityType1_idx` (`FacilityType_facility_id`),
  CONSTRAINT `fk_FacilitySubType_FacilityType1` FOREIGN KEY (`FacilityType_facility_id`) REFERENCES `facilitytype` (`facility_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilitysubtype`
--

LOCK TABLES `facilitysubtype` WRITE;
/*!40000 ALTER TABLE `facilitysubtype` DISABLE KEYS */;
INSERT INTO `facilitysubtype` VALUES (1,'badminton',0),(2,'swimming',0),(3,'basketball',0),(4,'climbing',0),(5,'personal training',0),(6,'squash',0),(7,'gerard hall',1),(8,'mini res',1),(9,'shireff hall',1),(10,'howe hall',1),(11,'risley hall',1),(12,'le marchant place',1),(13,'glengary apartment',1),(14,'graduate house',1),(15,'Killam Library',2),(16,'Sexton Library',2),(17,'MacRae Library',2),(18,'Kellog Library',2);
/*!40000 ALTER TABLE `facilitysubtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilitytype`
--

DROP TABLE IF EXISTS `facilitytype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilitytype` (
  `facility_id` int(11) NOT NULL,
  `facility_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`facility_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilitytype`
--

LOCK TABLES `facilitytype` WRITE;
/*!40000 ALTER TABLE `facilitytype` DISABLE KEYS */;
INSERT INTO `facilitytype` VALUES (0,'dalplex'),(1,'residence'),(2,'library'),(3,'international_centre');
/*!40000 ALTER TABLE `facilitytype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `faculty_id` int(11) NOT NULL,
  `faculty_name` varchar(100) DEFAULT NULL,
  `Campus_campus_id` int(11) NOT NULL,
  PRIMARY KEY (`faculty_id`),
  KEY `fk_Faculty_Campus1_idx` (`Campus_campus_id`),
  CONSTRAINT `fk_Faculty_Campus1` FOREIGN KEY (`Campus_campus_id`) REFERENCES `campus` (`campus_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (0,'Agriculture',1),(1,'Architecture and Planning',1),(2,'Arts and Social Sciences',1),(3,'College of Continuing Education',1),(4,'Computer Science',1),(5,'Dentistry',1),(6,'Engineering',1),(7,'Graduate Studies',1),(8,'Health',1),(9,'Law',1),(10,'Management',1),(11,'Medicine',1),(12,'Science',1);
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `internalfunding`
--

DROP TABLE IF EXISTS `internalfunding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internalfunding` (
  `id` int(11) NOT NULL,
  `type_of_grant` varchar(200) DEFAULT NULL,
  `ResearchOffice_office_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`ResearchOffice_office_id`),
  KEY `fk_InternalFunding_ResearchOffices1_idx` (`ResearchOffice_office_id`),
  CONSTRAINT `fk_InternalFunding_ResearchOffices1` FOREIGN KEY (`ResearchOffice_office_id`) REFERENCES `researchoffice` (`office_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internalfunding`
--

LOCK TABLES `internalfunding` WRITE;
/*!40000 ALTER TABLE `internalfunding` DISABLE KEYS */;
INSERT INTO `internalfunding` VALUES (0,'SSHRC Explore Grants Program',1),(1,'SSHRC Exchange Grants Program',1),(2,'Reduced salary for a research grant when NOT on leave',1),(3,'Supplemental sabbatical/special leave grant and leave remuneration',1),(4,'Supplemental educational/special educational leave grant and leave remuneration',1),(7,'Operations and Maintenance Response Fund (O and MRF) for Canada Foundation for Innovation (CFI) Projects',1),(8,'Ocean Frontier Institute: Seed Fund Program',1);
/*!40000 ALTER TABLE `internalfunding` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program`
--

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `program` (
  `program_id` int(11) NOT NULL,
  `program_name` varchar(100) DEFAULT NULL,
  `program_type` varchar(100) DEFAULT NULL,
  `Department_department_id` int(11) NOT NULL,
  PRIMARY KEY (`program_id`),
  KEY `fk_Program_Department1_idx` (`Department_department_id`),
  CONSTRAINT `fk_Program_Department1` FOREIGN KEY (`Department_department_id`) REFERENCES `department` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
INSERT INTO `program` VALUES (1,'BSc (Agriculture) in Agricultural Business','undergraduate',1),(2,'BSc (Agriculture) in Agricultural Economics','undergraduate',1),(3,'Bachelor of Agriculture International Food Business','undergraduate',1),(4,'Bachelor of Technology in Small Business Management','undergraduate',1),(5,'Diploma in Technology Business Management (DBM)','diploma',1),(6,'Certificate in International Rural Development','certificate',1),(7,'Certificate in Sustainable Development','certificate',1),(8,'Bachelor of Science (Agriculture) in Integrated Environmental Management','undergraduate',2),(9,'Engineering','undergraduate',2),(10,'Bachelor of Science (Agriculture) in Plant Science','undergraduate',3),(11,'Bachelor of Science (Agriculture) in Environmental Sciences','undergraduate',3),(12,'Bachelor of Technology in Environmental Landscape Horticulture','undergraduate',3),(13,'Bachelor of Technology in Landscape Architecture','undergraduate',3),(14,'Diploma in Technology Plant Science','certificates and diplomas',3),(15,'Diploma in Technology Managed Landscapes','certificates and diplomas',3),(16,'Master Gardener Training','certificates and diplomas',3),(17,'Certificate in Integrated Pest Management','certificates and diplomas',3),(18,'Post-Baccalaureate Certificate in Food Bioscience','certificates and diplomas',3),(19,'Post-Baccalaureate Certificate in Environmental Biology','certificates and diplomas',3),(20,'Bachelor of Science (Agriculture) in Animal Science','undergraduate',4),(21,'Bachelor of Science (Agriculture) in Aquaculture','undergraduate',4),(22,'Bachelor of Science in Bioveterinary Science','undergraduate',4),(23,'Pre-Veterinary Medicine','undergraduate',4),(24,'Master of Science (Agriculture), specializing in Animal Science or Aquaculture','graduate',4),(25,'Diploma in Technology - Veterinary Technology','certificates and diplomas',4),(26,'Diploma in Technology - Business Management','certificates and diplomas',4),(27,'Certificate in Animal Welfare','certificates and diplomas',4),(28,'Certificate in Aquaculture','certificates and diplomas',4),(29,'Certificate in Genetics and Molecular Biology','certificates and diplomas',4),(30,'Bachelor of Environmental Design Studies - BEDS','certificates and diplomas',5),(31,'Master of Architecture - MArch','certificates and diplomas',5),(32,'Bachelor of Community Design','undergraduate',6),(33,'Master of Planning','graduate',6),(34,'Master of Planning Studies','graduate',6),(35,'Interdisciplinary PhD','graduate',6),(36,'Minor in Biology','undergraduate',64),(37,'BSc 90-hour Minor in Biology','undergraduate',64),(38,'BA 90-hour Minor in Biology','undergraduate',64),(39,'BSc Major in Biology','undergraduate',64),(40,'BA Major in Biology','undergraduate',64),(41,'BSc Double Major in Biology and another subject','undergraduate',64),(42,'BA Double Major in Biology and another subject','undergraduate',64),(43,'BSc or BA Concentrated Honours in Biology','undergraduate',64),(44,'BSc or BA Combined Honours in Biology','undergraduate',64),(45,'Integrated Science Program','undergraduate',64),(46,'Co-op Program','undergraduate',64),(47,'Minor in Marine Biology','undergraduate',64),(48,'BSc Major in Marine Biology','undergraduate',64),(49,'BA Major in Marine Biology','undergraduate',64),(50,'BSc Double Major in Marine Biology and another subject','undergraduate',64),(51,'BA Double Major in Marine Biology and another subject','undergraduate',64),(52,'BSc or BA Concentrated Honours in Marine Biology','undergraduate',64),(53,'BSc or BA Combined Honours in Marine Biology','undergraduate',64),(54,'Integrated Science Program','undergraduate',64),(55,'MSc in Biology','masters',64),(56,'PhD in Biology','doctorate',64);
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `researchoffice`
--

DROP TABLE IF EXISTS `researchoffice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `researchoffice` (
  `office_id` int(11) NOT NULL,
  `office_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`office_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `researchoffice`
--

LOCK TABLES `researchoffice` WRITE;
/*!40000 ALTER TABLE `researchoffice` DISABLE KEYS */;
INSERT INTO `researchoffice` VALUES (1,'Office of Research Services (ORS)');
/*!40000 ALTER TABLE `researchoffice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `professor_id` int(11) NOT NULL,
  `professor_first_name` varchar(100) DEFAULT NULL,
  `professor_last_name` varchar(100) DEFAULT NULL,
  `professor_email` varchar(100) DEFAULT NULL,
  `Faculty_faculty_id` int(11) NOT NULL,
  PRIMARY KEY (`professor_id`),
  KEY `fk_Professor_Faculty1_idx` (`Faculty_faculty_id`),
  CONSTRAINT `fk_Professor_Faculty1` FOREIGN KEY (`Faculty_faculty_id`) REFERENCES `faculty` (`faculty_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'Greg','Cameron','gregory.cameron@dal.ca',0),(2,'Sylvain','Charlebois','sylvain.charlebois@dal.ca',0),(3,'Stephen','Clark','jsclark@dal.ca',0),(4,'Steven','Dukeshire','steven.dukeshire@dal.ca',0),(5,'Diane','Dunlop','diane.dunlop@dal.ca',0),(6,'Gary','Grant','kggrant@dal.ca',0),(7,'Heather‐Anne','Grant','h.grant@dal.ca',0),(8,'Iona','Green','iona.green@dal.ca',0),(9,'Christopher','Hartt','chris.hartt@dal.ca',0),(10,'Kathleen','Kevany','kkevany@dal.ca',0),(11,'Ji','Lu','ji.lu@dal.ca',0),(12,'Tasha','Richard','tasha.richard@dal.ca',0),(13,'Deborah','Stiles','deborah.stiles@dal.ca',0),(14,'Emmanuel','Yiridoe','emmanuel.yiridoe@dal.ca',0),(15,'Ahmad','Al-Mallahi','ahmad.almallahi@dal.ca',0),(16,'Tess','Astatkie','astatkie@dal.ca',0),(17,'Young','Ki-Chang','youngchang@dal.ca',0),(18,'Travis','Esau','tesau@dal.ca',0),(19,'Peter','Havard','phavard@dal.ca',0),(20,'Sophia','He','quan.he@dal.ca',0),(21,'Alex','Martynenko','alex.martynenko@dal.ca',0),(22,'Chris','Nelson','c.nelson@dal.ca',0),(23,'Pat','Nelson','pnelson@dal.ca',0),(24,'Tri','Nguyen‐Quang','tri.nguyen-quang@dal.ca',0),(25,'Haibo','Niu','haibo.niu@dal.ca',0),(26,'Gordon','Price','gprice@dal.ca',0),(27,'Scott','Read','scott.read@dal.ca',0),(28,'Jin','Yue','jyue@dal.ca',0),(29,'Qamar','Zaman','qzaman@dal.ca',0),(30,'Lord','Abbey','labbey@dal.ca',0),(31,'Samuel','Asiedu','sasiedu@dal.ca',0),(32,'Nandika','Bandara','bandara@dal.ca',0),(33,'Heather','Braiden','heather.braiden@dal.ca',0),(34,'David','Burton','dburton@dal.ca',0),(35,'Sherry','Chaisson','sherry.chaisson@dal.ca',0),(36,'Christopher','Cutler','chris.cutler@dal.ca',0),(37,'Fred','Fergus','fred.fergus@dal.ca',0),(38,'Robert','France','rfrance@dal.ca',0),(39,'Andrew','Hammermeister','andrew.hammermeister@dal.ca',0),(40,'Deborah','Adewole','deborah.adewole@dal.ca',0),(41,'Derek','Anderson','danderson@dal.ca',0),(42,'David','Barrett','david.barrett@dal.ca',0),(43,'Amy','Birchall','amy.birchall@dal.ca',0),(44,'Fraser','Clark','fraser.clark@dal.ca',0),(45,'Stephanie','Collins','s.collins@dal.ca',0),(46,'Stefanie','Colombo','scolombo@dal.ca',0),(47,'Jim','Duston','jduston@dal.ca',0),(48,'Hossain','Farid','ah.farid@dal.ca',0),(49,'Gillian','Fraser','gillian.Fraser@Dal.Ca',0),(50,'Alan','Fredeen','alan.fredeen@dal.ca',0),(51,'Sarah','Gatti‐Yorke','Sarah.Gatti-Yorke@Dal.Ca',0),(52,'Dr.','Miriam-Gordon','miriam.gordon@dal.ca',0),(53,'Janine','Gray','janine.gray@dal.ca',0),(54,'Margie','Hartling','MHartling@Dal.Ca',0),(55,'Scott','Jeffrey','scott.jeffrey@dal.ca',0),(56,'Laurel','MacIntosh','Laurel.MacIntosh@Dal.Ca',0),(57,'Marla','MacKay','marla.mackay@dal.ca',0),(58,'Leslie','MacLaren','leslie.maclaren@dal.ca',0),(59,'Audrie‐Jo','McConkey','amcconkey@dal.ca',0),(60,'Younes','Miar','miar@dal.ca',0),(61,'Lori','Parsons','lori.parsons@dal.ca',0),(62,'Dian','Patterson','dian.patterson@dal.ca',0),(63,'Dara','Pelkey‐Field','dpelkey@dal.ca',0),(64,'Bruce','Rathgeber','brathgeber@dal.ca',0),(65,'Chastity','Spears','cspears@dal.ca',0),(66,'Sarah','Stewart‐Clark','sarah.stewart-clark@dal.ca',0),(67,'Sarah','Bonnemaison','sarah.bonnemaison@dal.ca',1),(68,'Diogo','Burnay','diogo.burnay@dal.ca',1),(69,'Ted','Cavanagh','ted.cavanagh@dal.ca',1),(70,'Elisa','Dainese','elisa.dainese@dal.ca',1),(71,'Susan','Fitzgerald','susan.fitzgerald@dal.ca',1),(72,'James','Forren','james.forren@dal.ca',1),(73,'Emanuel','Jannasch','jannasch@dal.ca',1),(74,'Brian','Lilley','brian.lilley@dal.ca',1),(75,'Brian','MacKay‐Lyons','brian@mlsarchitects.ca',1),(76,'Christine','Macy','christine.macy@dal.ca',1),(77,'Steven','Mannell','steven.mannell@dal.ca',1),(78,'Roger','Mullin','roger.mullin@dal.ca',1),(79,'Stephen','Parcell','parcell@dal.ca',1),(80,'Austin','Parsons','austin.parsons@dal.ca',1),(81,'Niall','Savage','niall.savage@dal.ca',1),(82,'Talbot','Sweetapple','talbot@mlsarchitects.ca',1),(83,'Catherine','Venart','cvenart@dal.ca',1),(84,'Cristina','Verissimo','cristina.verissimo@dal.ca',1),(85,'Grant','Wanzel','grant.wanzel@dal.ca',1),(86,'Ahsan','Habib','ahsan.habib@dal.ca',1),(87,'Patricia','Manuel','patricia.manuel@dal.ca',1),(88,'Eric','Rapaport','eric.rapaport@dal.ca',1),(89,'Mikiko','Terashima','mikiko.terashima@dal.ca',1),(90,'Ren','Thomas','ren.thomas@dal.ca',1),(91,'Lisa','Berglund','lisa.berglund@dal.ca',1),(92,'Joseli','Macedo','Dean.AP@dal.ca',1),(93,'Jill','Grant','jill.grant@dal.ca',1),(94,'Frank','Palermo','frank.palermo@dal.ca',1),(95,'Paul','Bentzen','paul.bentzen@dal.ca',12),(96,'Erin','Bertrand','erin.bertrand@dal.ca',12),(97,'Joseph','Bielawski','j.bielawski@dal.ca',12),(98,'Patrice','Côté','patrice@dal.ca',12),(99,'Glenn','Crossin','gtc@dal.ca',12),(100,'Arunika','Gunawardena','arunika.gunawardena@dal.ca',12),(101,'Christophe','Herbinger','christophe.herbinger@dal.ca',12),(102,'Jeffrey','Hutchings','jeff.hutchings@dal.ca',12),(103,'Sara','Iverson','sara.iverson@dal.ca',12),(104,'Mark','Johnston','mark.johnston@dal.ca',12),(105,'Patricia','Lane','patricia.lane@dal.ca',12),(106,'Julie','Laroche','Julie.Laroche@Dal.Ca',12),(107,'Robert','Latta','robert.latta@dal.ca',12),(108,'Marty','Leonard','marty.leonard@dal.ca',12),(109,'Heike','Lotze','heike.lotze@dal.ca',12),(110,'Aaron','Macneil','a.macneil@dal.ca',12),(111,'Daniel','Ruzzante','Ruzzante@dal.ca',12),(112,'Alastair','Simpson','alastair.simpson@dal.ca',12),(113,'Sophia','Stone','sophia.stone@dal.ca',12),(114,'Derek','Tittensor','Derek.Tittensor@unep-wcmc.org',12),(115,'Sandra','Walde','sandra.walde@dal.ca',12),(116,'Hal','Whitehead','hal.whitehead@dal.ca',12),(117,'Boris','Worm','bworm@dal.ca',12);
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-27  3:35:27
