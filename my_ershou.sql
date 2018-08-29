DROP TABLE IF EXISTS `ershou`;

CREATE TABLE `ershou` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `city` varchar(10) DEFAULT NULL,
  `modify_date` varchar(8) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  `xiaoqu` varchar(50) DEFAULT NULL,
  `huxing` varchar(50) DEFAULT NULL,
  `mianji` DECIMAL(8,2) DEFAULT NULL,
  `chaoxiang` varchar(50) DEFAULT NULL,
  `zhuangxiu` varchar(50) DEFAULT NULL,
  `dianti` varchar(50) DEFAULT NULL,
  `describes` varchar(100) DEFAULT NULL,
  `totalprice` int(11) DEFAULT NULL,
  `unitprice` int(11) DEFAULT NULL,
  `loucheng` varchar(50) DEFAULT NULL,
  `height` varchar(50) DEFAULT NULL,
  `niandai` timestamp DEFAULT CURRENT_TIMESTAMP,
  `guanzhu` int(11) DEFAULT NULL,
  `daikan` int(11) DEFAULT NULL,
  `fabushijian` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

