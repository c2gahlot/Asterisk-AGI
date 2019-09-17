# ************************************************************
# Sequel Pro SQL dump
# Version 5425
#
# https://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.18-0ubuntu0.16.04.1)
# Database: my_operator
# Generation Time: 2019-09-17 11:26:05 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table agents
# ------------------------------------------------------------

DROP TABLE IF EXISTS `agents`;

CREATE TABLE `agents` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `company_id` int(11) unsigned NOT NULL,
  `tags` varchar(255) NOT NULL DEFAULT '',
  `type` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `agents` WRITE;
/*!40000 ALTER TABLE `agents` DISABLE KEYS */;

INSERT INTO `agents` (`id`, `company_id`, `tags`, `type`, `name`)
VALUES
	(1,1,'sales','SIP','sales'),
	(2,1,'support','SIP','support');

/*!40000 ALTER TABLE `agents` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table callers
# ------------------------------------------------------------

DROP TABLE IF EXISTS `callers`;

CREATE TABLE `callers` (
  `dnid` varchar(11) NOT NULL DEFAULT '',
  `company_id` int(11) unsigned NOT NULL,
  PRIMARY KEY (`dnid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `callers` WRITE;
/*!40000 ALTER TABLE `callers` DISABLE KEYS */;

INSERT INTO `callers` (`dnid`, `company_id`)
VALUES
	('100',1),
	('101',2),
	('102',1);

/*!40000 ALTER TABLE `callers` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table companies
# ------------------------------------------------------------

DROP TABLE IF EXISTS `companies`;

CREATE TABLE `companies` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;

INSERT INTO `companies` (`id`, `name`)
VALUES
	(1,'My Operator'),
	(2,'GetMeCab');

/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ivr_node_input_maps
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ivr_node_input_maps`;

CREATE TABLE `ivr_node_input_maps` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ivr_node_id` int(11) unsigned NOT NULL,
  `input` int(11) unsigned NOT NULL,
  `ivr_id` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `ivr_node_input_maps` WRITE;
/*!40000 ALTER TABLE `ivr_node_input_maps` DISABLE KEYS */;

INSERT INTO `ivr_node_input_maps` (`id`, `ivr_node_id`, `input`, `ivr_id`)
VALUES
	(1,2,1,4),
	(2,2,2,5),
	(3,6,1,6),
	(4,6,2,7);

/*!40000 ALTER TABLE `ivr_node_input_maps` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ivr_node_settings
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ivr_node_settings`;

CREATE TABLE `ivr_node_settings` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ivr_node_id` int(11) unsigned NOT NULL,
  `action` varchar(255) NOT NULL DEFAULT '',
  `file` varchar(255) DEFAULT NULL,
  `user` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `ivr_node_settings` WRITE;
/*!40000 ALTER TABLE `ivr_node_settings` DISABLE KEYS */;

INSERT INTO `ivr_node_settings` (`id`, `ivr_node_id`, `action`, `file`, `user`)
VALUES
	(1,1,'playback','/home/vagrant/code/Asterisk-AGI/storage/audios/welcome',NULL),
	(2,2,'input',NULL,NULL),
	(3,3,'playback','/home/vagrant/code/Asterisk-AGI/storage/audios/redirect_sales',NULL),
	(4,4,'dial',NULL,'SIP/sales'),
	(5,5,'playback','/home/vagrant/code/Asterisk-AGI/storage/audios/confirmation_support',NULL),
	(6,6,'input',NULL,NULL),
	(7,7,'playback','/home/vagrant/code/Asterisk-AGI/storage/audios/redirect_support',NULL),
	(8,8,'dial',NULL,'SIP/support'),
	(9,9,'hangup',NULL,NULL);

/*!40000 ALTER TABLE `ivr_node_settings` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ivr_nodes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ivr_nodes`;

CREATE TABLE `ivr_nodes` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ivr_id` int(10) unsigned NOT NULL,
  `node_name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `ivr_nodes` WRITE;
/*!40000 ALTER TABLE `ivr_nodes` DISABLE KEYS */;

INSERT INTO `ivr_nodes` (`id`, `ivr_id`, `node_name`)
VALUES
	(1,1,'play_intro'),
	(2,1,'select_department'),
	(3,4,'play_connecting_sales'),
	(4,4,'connecting_sales'),
	(5,5,'play_connecting_support'),
	(6,5,'connecting_support_confirmation'),
	(7,6,'play_connecting_support'),
	(8,6,'connecting_support'),
	(9,7,'hangup');

/*!40000 ALTER TABLE `ivr_nodes` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ivrs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ivrs`;

CREATE TABLE `ivrs` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `context` varchar(255) NOT NULL DEFAULT '',
  `company_id` int(11) unsigned NOT NULL,
  `name` varchar(255) NOT NULL DEFAULT '',
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `ivrs` WRITE;
/*!40000 ALTER TABLE `ivrs` DISABLE KEYS */;

INSERT INTO `ivrs` (`id`, `context`, `company_id`, `name`, `start_time`, `end_time`)
VALUES
	(1,'incoming',1,'day','06:00:00','18:00:00'),
	(2,'incoming',1,'night','18:00:00','06:00:00'),
	(3,'incoming',2,'anytime','00:00:00','00:00:00'),
	(4,'contact_sales',1,'sales_anytime','00:00:00','00:00:00'),
	(5,'contact_support',1,'support_anytime','00:00:00','00:00:00'),
	(6,'continue_calling_support',1,'continue_support_anytime','00:00:00','00:00:00'),
	(7,'stop_calling_support',1,'stopping_support_anytime','00:00:00','00:00:00');

/*!40000 ALTER TABLE `ivrs` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
