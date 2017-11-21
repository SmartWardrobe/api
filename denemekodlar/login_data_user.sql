-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: localhost    Database: login_data
-- ------------------------------------------------------
-- Server version	5.7.12-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'tugce1','tugce2','tugce3'),(2,'tugce4','tugce5','tugce6'),(3,'tugba','tug','tugbactky'),(4,'tugba','tug','tugbactky'),(5,'zekayi','zek1','zek57'),(6,'zekayi','zek1','zek57'),(7,'tugba','tug','tutu'),(8,'tugba','tug','ttu'),(9,'tugba','tug','tugce.ctky@gmail.com'),(10,'tugba','tug','tugce.ctky@gmail.com'),(11,'','','tugce.ctky@gmail.com'),(12,'tugba','tug','tugce.ctky@gmail.com'),(13,'tubili','1234','tubilima'),(14,'nez','nez1','nez123'),(15,'toprak','che','nora'),(16,'tutu','666','heh'),(17,'deneme','357','eposta'),(18,'deneme','357','eposta'),(19,'xyz','13579','habarabuhaba'),(20,'xyz','222','habarabuhaba'),(21,'ghgh','hghgh','ghgh'),(22,'ffgg','jfjfj','djdjd'),(23,'nezahat','nezahat123','nezahat@gmail.com'),(24,'tuba','pbkdf2:sha256:50000$fI2bE79l$4d90b656c95ce0f76c822bcc717818c0e2e4658ce94796ce21d7ad69a5d58372','tuba@gmail.com'),(25,'tugba','pbkdf2:sha256:50000$LFLjL70a$9e74749e21de49247136cdb0a5cc876dd177b216d57255b450585d1da5bfaa61','tugce.ctky@gmail.com'),(26,'tugba','pbkdf2:sha256:50000$qJjlTD99$c26011338152e4b422f77adc77a4a0ed302e536dcfc593db83849ec2f0985213','tugce.ctky@gmail.com'),(27,'tugba','pbkdf2:sha256:50000$OK4VW2iu$66c60883e6d2805969be61352225f202b30a19ffd6858088b941950391fe6a28','tugce.ctky@gmail.com'),(28,'deneme','pbkdf2:sha256:50000$C1PyrAsG$39b9fdbf6cae79ddb7c7aee2f1c622659ce683d4dfeb4b855e270ed0b3e05834','tugce.ctky@gmail.com'),(29,'sdfe','pbkdf2:sha256:50000$F7etzUqp$934cf8167fcf38c342a5b14f013b8d5956a005f95c16055041e272f3087dcadf','tugce.ctky@gmail.com'),(30,'ytyy','pbkdf2:sha256:50000$HYUg60JD$95454512286372589d2aa96c99e8ef9271cd93b1155fc791cae9ea3916569a2f','tuba@gmail.com'),(31,'tuti','pbkdf2:sha256:50000$WB0KRnFz$12686430ed7a0dc2facdbaeebc2fcaccc63b824f3d9b87c0c8a2919c02f2fd83','cici@gmail.com'),(32,'tugba','pbkdf2:sha256:50000$R6aEUO1h$2d9e544597b23faa7968af15d101ca1007154baf2247bcf4b39a2c3d77a9249a','tugce.ctky@gmail.com');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-19 16:31:19
