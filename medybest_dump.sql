-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: medybest
-- ------------------------------------------------------
-- Server version	8.0.25

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
-- Table structure for table `company_table`
--

DROP TABLE IF EXISTS `company_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_table` (
  `Sr_no` int NOT NULL AUTO_INCREMENT,
  `Company_name` varchar(200) DEFAULT NULL,
  `Contact_person` varchar(50) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Contact_no` bigint DEFAULT NULL,
  `Entry_date` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Sr_no`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_table`
--

LOCK TABLES `company_table` WRITE;
/*!40000 ALTER TABLE `company_table` DISABLE KEYS */;
INSERT INTO `company_table` VALUES (3,'Vicks','Anubhav Parmar','Somwhere, Gujarat, India','vickspvtltd@gmail.com',6896568515,'2021-7-18'),(5,'Himalaya','Amol Kumar','Somewhere, Gujarat, India','amolkumar323@gmail.com',6876598654,'2021-7-18'),(6,'lirils','Arjun shrma','somewhere, gujarat, india','something@gmail.com',1234568970,'2021-10-14');
/*!40000 ALTER TABLE `company_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicine_table`
--

DROP TABLE IF EXISTS `medicine_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicine_table` (
  `Sr_no` int NOT NULL AUTO_INCREMENT,
  `Medicine_Name` varchar(100) DEFAULT NULL,
  `Quantity` int DEFAULT NULL,
  `Batch_no` int DEFAULT NULL,
  `Category` varchar(50) DEFAULT NULL,
  `Manufacturer` varchar(100) DEFAULT NULL,
  `Production_Date` varchar(10) DEFAULT NULL,
  `Expiry_Date` varchar(10) DEFAULT NULL,
  `Entry_Date` varchar(10) DEFAULT NULL,
  `Buying_price` decimal(10,2) DEFAULT NULL,
  `Selling_price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Sr_no`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicine_table`
--

LOCK TABLES `medicine_table` WRITE;
/*!40000 ALTER TABLE `medicine_table` DISABLE KEYS */;
INSERT INTO `medicine_table` VALUES (1,'Vicks',5000,532342,'Tablet','vicks.pvt.ltd','2021-7-7','2023-7-14','2021-7-14',2000.00,5000.00),(4,'Glucometer',20,643463,'Medical Equipment','Dr. Trust','2021-7-17','2021-7-17','2021-7-17',10000.00,36000.00),(5,'Paracetamol',500,434234,'Tablet','medstore.pvt.ltd','2021-7-1','2023-7-28','2021-7-14',750.00,1500.00),(6,'Deodrant',100,734522,'Medical Material','cintol.pvt.ltd','2021-5-12','2021-7-14','2021-7-14',4000.00,3000.00),(7,'Protein +',50,683824,'Medical Material','protienplus.pvt.ltd','2021-4-21','2021-7-14','2021-7-14',20000.00,37500.00),(8,'Disprine',200,1231231,'Tablet','UAR pvt. ltd.','2021-7-2','2021-7-14','2021-7-14',300.00,700.00),(9,'Vitamin D 50,000 IU',500,349523,'Tablet','Vitmole. pvt. ltd.','2021-4-14','2021-7-14','2021-7-14',5000.00,8000.00),(10,'Doxycycline',100,524933,'Injection','AXW pvt.ltd.','2021-7-18','2021-7-18','2021-7-18',2500.00,3500.00),(11,'Head & Shoulders 500ml',20,743454,'Medical Material','head&shoulders.pvt.','2021-4-5','2023-7-4','2021-7-14',4000.00,7440.00),(13,'Deodrant',100,734522,'Medical Material','cintol.pvt.ltd','2021-5-12','2021-7-14','2021-7-14',2000.00,3000.00),(14,'Candid Dusting Powder',20,3243234,'Medical Material','GenMark','2020-7-15','2023-7-6','2021-7-17',1200.00,85.00),(15,'Enauniq',50,230,'Medical Material','ENA Universal','2022-5-18','2022-5-18','2022-5-18',7500.00,250.00),(16,'Penakam Gel',100,345,'Medical Material','Lexine','2020-8-14','2023-7-13','2021-7-17',2000.00,60.00),(17,'Diovol 170ml (Mint Flavor)',50,34234,'Syrub','Wallace pvt.ltd.','2021-8-18','2021-7-17','2021-7-23',3000.00,114.00),(18,'Herbalife Nutrition (300g) lemon Flovor',20,3244323,'Medical Material','Herbalife pvt.ltd.','2021-7-17','2021-7-17','2021-7-17',30000.00,6032.00),(19,'Johnson\'s Buds 75n stems',100,234321,'Medical Material','Johnsons & Johnson','2021-1-1','2025-7-17','2021-7-17',3000.00,90.00),(20,'Vaseline Cocoa Glow 100ml',50,12312,'Medical Material','HINDUSTAN UNILEVER','2021-7-17','2021-7-17','2021-7-17',3000.00,99.00),(21,'X-MEN Aqua 100ml',20,1231223,'Medical Material','Celine Health Care','2019-6-6','2022-5-19','2021-7-17',2000.00,210.00),(22,'Clean and clear',100,58468,'Medical Material','clean&clearpvt.ltd.','2021-7-18','2021-7-18','2021-7-18',5000.00,60.00),(23,'Daimox',200,484842,'Medical Material','jksdhfindn.pvt.ltd.','2019-7-11','2022-7-12','2021-7-18',5000.00,120.00);
/*!40000 ALTER TABLE `medicine_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_info`
--

DROP TABLE IF EXISTS `sales_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_info` (
  `Sr_no` int NOT NULL AUTO_INCREMENT,
  `Customer_Name` varchar(50) DEFAULT NULL,
  `Phone_Number` bigint DEFAULT NULL,
  `Time` varchar(50) DEFAULT NULL,
  `Date` varchar(50) DEFAULT NULL,
  `Net_Total` decimal(50,2) DEFAULT NULL,
  `Gross_total` decimal(50,2) DEFAULT NULL,
  `Discount` decimal(50,2) DEFAULT NULL,
  `Payment_mode` varchar(50) DEFAULT NULL,
  `Paid_amount` decimal(50,2) DEFAULT NULL,
  `Return_amount` decimal(50,2) DEFAULT NULL,
  PRIMARY KEY (`Sr_no`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_info`
--

LOCK TABLES `sales_info` WRITE;
/*!40000 ALTER TABLE `sales_info` DISABLE KEYS */;
INSERT INTO `sales_info` VALUES (1,'Shivam',9984628222,'04:50:52 PM','17, 07 2021',608.00,618.00,10.00,'Google Pay',608.00,0.00),(2,'ashish',1231231321,'06:28:25 PM','17, 07 2021',213.00,213.00,0.00,'Google Pay',213.00,0.00),(3,'Prem',9759656651,'07:38:16 PM','17, 07 2021',472.00,472.00,0.00,'Cash',500.00,28.00),(4,'Aditya',8794654854,'07:44:47 PM','17, 07 2021',1154.00,1154.00,0.00,'Cash',2000.00,846.00),(5,'afsdf',2342342423,'07:55:25 PM','17, 07 2021',384.00,384.00,0.00,'Cash',400.00,16.00),(6,'Dimple',9871238732,'08:00:08 PM','17, 07 2021',490.00,500.00,10.00,'Cash',500.00,10.00),(7,'Ansita',9756546542,'08:52:59 PM','17, 07 2021',1785.00,1785.00,0.00,'Google Pay',1785.00,0.00),(8,'Nishant',7686764563,'08:56:42 PM','17, 07 2021',369.00,369.00,0.00,'Cash',400.00,31.00),(9,'Parth',9876578673,'08:59:31 PM','17, 07 2021',620.00,620.00,0.00,'Cash',700.00,80.00),(10,'Harikrushan',9867876987,'09:07:08 PM','17, 07 2021',1288.00,1288.00,0.00,'Google Pay',1288.00,0.00),(11,'Ansh',9875349874,'09:09:40 PM','17, 07 2021',711.00,711.00,0.00,'Google Pay',711.00,0.00),(12,'Mankumar',9876646566,'09:12:47 PM','17, 07 2021',150.00,150.00,0.00,'Debit Card',150.00,0.00),(13,'Arjun',8974052844,'09:19:41 PM','17, 07 2021',1000.00,1020.00,20.00,'Paytm',1000.00,0.00),(14,'Kshipra',9048503944,'09:25:05 PM','17, 07 2021',1360.00,1360.00,0.00,'Credit Card',1360.00,0.00),(15,'Shubham',4523445344,'09:28:19 PM','17, 07 2021',1190.00,1190.00,0.00,'Google Pay',1190.00,0.00),(16,'Nayan',8749832384,'09:31:12 PM','17, 07 2021',1387.00,1417.00,30.00,'Cash',1500.00,113.00),(17,'Saurabh',8498437983,'09:33:11 PM','17, 07 2021',38130.00,38130.00,0.00,'Google Pay',38130.00,0.00),(18,'akshay',6756456456,'09:35:29 PM','17, 07 2021',3680.00,3680.00,0.00,'Cash',3580.00,0.00),(19,'Abhay',9845783434,'10:06:06 PM','17, 07 2021',1039.00,1039.00,0.00,'Google Pay',1039.00,0.00),(20,'Mayank',2342334234,'10:07:51 PM','17, 07 2021',358.00,358.00,0.00,'Cash',500.00,142.00),(21,'Ankit',3453232323,'10:11:15 PM','17, 07 2021',5285.00,5285.00,0.00,'Google Pay',5285.00,0.00),(22,'sdkfjskd',9403266843,'10:13:05 PM','17, 07 2021',3250.00,3250.00,0.00,'Paytm',3250.00,0.00),(23,'fdgdsga',7878787878,'10:14:55 PM','17, 07 2021',85.00,85.00,0.00,'Google Pay',85.00,0.00),(24,'asdfsd',4353435345,'10:16:42 PM','17, 07 2021',3000.00,3000.00,0.00,'Credit Card',3000.00,0.00),(25,'asdfadffd',2134234234,'10:19:40 PM','17, 07 2021',114.00,114.00,0.00,'Google Pay',114.00,0.00),(26,'Kruti',9886455625,'10:22:29 PM','17, 07 2021',1335.00,1335.00,0.00,'Paytm',1335.00,0.00),(27,'Shruti',7656454334,'12:13:57 AM','18, 07 2021',1157.00,1157.00,0.00,'Google Pay',1157.00,0.00),(28,'Shruti',7656454334,'12:14:13 AM','18, 07 2021',1157.00,1157.00,0.00,'Google Pay',1157.00,0.00),(29,'Alan',6878688195,'03:36:26 AM','18, 07 2021',6212.00,6212.00,0.00,'Cash',6500.00,288.00),(30,'Michael',8948968918,'03:37:31 AM','18, 07 2021',375.00,375.00,0.00,'Google Pay',375.00,0.00),(31,'John',8987825871,'03:42:05 AM','18, 07 2021',339.00,339.00,0.00,'Credit Card',399.00,0.00),(32,'Dev',9879856861,'03:44:57 AM','18, 07 2021',235.00,235.00,0.00,'Paytm',235.00,0.00),(33,'Aryan',9674565456,'04:12:13 AM','18, 07 2021',1650.00,1650.00,0.00,'Paytm',1650.00,0.00),(34,'Kiran',7789678785,'04:16:29 AM','18, 07 2021',9500.00,9500.00,0.00,'Credit Card',9500.00,0.00),(35,'vatsal',8975266158,'04:20:11 AM','18, 07 2021',420.00,420.00,0.00,'Google Pay',420.00,0.00),(36,'dfsd',7897845645,'04:21:19 AM','18, 07 2021',1175.00,1175.00,0.00,'Credit Card',1175.00,0.00),(37,'Johnny',9875648615,'05:50:27 AM','18, 07 2021',3310.00,3360.00,50.00,'Cash',3310.00,0.00),(38,'aaman',9684681681,'09:00:27 PM','18, 07 2021',544.00,554.00,10.00,'Google Pay',544.00,0.00),(39,'ajay',8979864865,'10:07:18 PM','18, 07 2021',1155.00,1155.00,0.00,'Cash',1200.00,45.00),(40,'aniruthjf',3243023893,'06:54:07 AM','11, 09 2021',85.00,85.00,0.00,'Google Pay',85.00,0.00);
/*!40000 ALTER TABLE `sales_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff_table`
--

DROP TABLE IF EXISTS `staff_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff_table` (
  `Sr_no` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) DEFAULT NULL,
  `Age` int DEFAULT NULL,
  `Gender` varchar(25) DEFAULT NULL,
  `Marital_status` varchar(50) DEFAULT NULL,
  `Blood_group` varchar(3) DEFAULT NULL,
  `Address` varchar(250) DEFAULT NULL,
  `Date_of_birth` varchar(10) DEFAULT NULL,
  `Joining_date` varchar(10) DEFAULT NULL,
  `Contact_no` bigint DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Aadhar_no` bigint DEFAULT NULL,
  `Salary` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Sr_no`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_table`
--

LOCK TABLES `staff_table` WRITE;
/*!40000 ALTER TABLE `staff_table` DISABLE KEYS */;
INSERT INTO `staff_table` VALUES (2,'Prem',18,'Male','Single','O+','Somewhere, Vadodara, Gujarat','2021-7-18','2021-7-18',7889546542,'premshilu2002@gmail.com',789446551325,15000.00),(3,'Ashish',18,'Male','Single','A+','Somewhere, Vadodara, Gujarat','2021-7-18','2021-7-18',7567956523,'ashishkumarpatel2003@gmail.com',879569865165,10000.00),(4,'aman',18,'Male','Single','B+','somewhere','2000-1-13','2021-7-8',8481989654,'amanpatel@gmail.com',897519816814,10000.00),(5,'Shivam',18,'Male','Single','B+','somewhere, gujarat, India','2001-4-4','2021-7-18',8496541864,'shivamzala@gamil.com',899846548644,1000000.00);
/*!40000 ALTER TABLE `staff_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-18 18:59:08
