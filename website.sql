-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 06, 2019 at 12:41 AM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.1.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `website`
--
CREATE DATABASE IF NOT EXISTS `website` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `website`;

DELIMITER $$
--
-- Functions
--
DROP FUNCTION IF EXISTS `URLDECODER`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `URLDECODER` (`str` VARCHAR(4096) CHARSET utf8) RETURNS VARCHAR(4096) CHARSET latin1 BEGIN
               DECLARE X  INT;               
               DECLARE chr VARCHAR(256);
               DECLARE chrto VARCHAR(256);
               DECLARE result VARCHAR(4096);
               SET X = 1;
               WHILE X  <= (SELECT MAX(id) FROM urlcodemap) DO
                   SET chr = (SELECT `encoded` FROM urlcodemap WHERE id = X);
                   SET chrto = (SELECT `decoded` FROM urlcodemap WHERE id = X);                
                           SET str = REPLACE(str,chr,chrto);
                           SET  X = X + 1;                           
               END WHILE;
               RETURN str;
       END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `gifts`
--

DROP TABLE IF EXISTS `gifts`;
CREATE TABLE `gifts` (
  `id` int(255) NOT NULL,
  `name` varchar(255) CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL,
  `descr` varchar(255) CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gifts`
--

INSERT INTO `gifts` (`id`, `name`, `descr`) VALUES
(1, 'Very strong computer', 'very very very good pc');

-- --------------------------------------------------------

--
-- Table structure for table `urlcodemap`
--

DROP TABLE IF EXISTS `urlcodemap`;
CREATE TABLE `urlcodemap` (
  `id` int(11) NOT NULL,
  `encoded` varchar(128) NOT NULL,
  `decoded` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `urlcodemap`
--

INSERT INTO `urlcodemap` (`id`, `encoded`, `decoded`) VALUES
(1, '%20', ' '),
(2, '%21', '!'),
(3, '%22', '\"'),
(4, '%23', '#'),
(5, '%24', '$'),
(6, '%25', '%'),
(7, '%26', '&'),
(8, '%27', '\''),
(9, '%28', '('),
(10, '%29', ')'),
(11, '%2A', '*'),
(12, '%2B', '+'),
(13, '%2C', ','),
(14, '%2D', '-'),
(15, '%2E', '.'),
(16, '%2F', '/'),
(17, '%30', '0'),
(18, '%31', '1'),
(19, '%32', '2'),
(20, '%33', '3'),
(21, '%34', '4'),
(22, '%35', '5'),
(23, '%36', '6'),
(24, '%37', '7'),
(25, '%38', '8'),
(26, '%39', '9'),
(27, '%3A', ':'),
(28, '%3B', ';'),
(29, '%3C', '<'),
(30, '%3D', '='),
(31, '%3E', '>'),
(32, '%3F', '?'),
(33, '%40', '@'),
(34, '%41', 'A'),
(35, '%42', 'B'),
(36, '%43', 'C'),
(37, '%44', 'D'),
(38, '%45', 'E'),
(39, '%46', 'F'),
(40, '%47', 'G'),
(41, '%48', 'H'),
(42, '%49', 'I'),
(43, '%4A', 'J'),
(44, '%4B', 'K'),
(45, '%4C', 'L'),
(46, '%4D', 'M'),
(47, '%4E', 'N'),
(48, '%4F', 'O'),
(49, '%50', 'P'),
(50, '%51', 'Q'),
(51, '%52', 'R'),
(52, '%53', 'S'),
(53, '%54', 'T'),
(54, '%55', 'U'),
(55, '%56', 'V'),
(56, '%57', 'W'),
(57, '%58', 'X'),
(58, '%59', 'Y'),
(59, '%5A', 'Z'),
(60, '%5B', '['),
(61, '%5C', '\\'),
(62, '%5D', ']'),
(63, '%5E', '^'),
(64, '%5F', '_'),
(65, '%60', '`'),
(66, '%61', 'a'),
(67, '%62', 'b'),
(68, '%63', 'c'),
(69, '%64', 'd'),
(70, '%65', 'e'),
(71, '%66', 'f'),
(72, '%67', 'g'),
(73, '%68', 'h'),
(74, '%69', 'i'),
(75, '%6A', 'j'),
(76, '%6B', 'k'),
(77, '%6C', 'l'),
(78, '%6D', 'm'),
(79, '%6E', 'n'),
(80, '%6F', 'o'),
(81, '%70', 'p'),
(82, '%71', 'q'),
(83, '%72', 'r'),
(84, '%73', 's'),
(85, '%74', 't'),
(86, '%75', 'u'),
(87, '%76', 'v'),
(88, '%77', 'w'),
(89, '%78', 'x'),
(90, '%79', 'y'),
(91, '%7A', 'z'),
(92, '%7B', '{'),
(93, '%7C', '|'),
(94, '%7D', '}'),
(95, '%7E', '~'),
(96, '%80', '`'),
(97, '%82', ','),
(98, '%83', 'ƒ'),
(99, '%84', ','),
(100, '%85', '.'),
(101, '%86', '+'),
(102, '%87', 'Ï'),
(103, '%88', '^'),
(104, '%89', '%'),
(105, '%8A', 'S'),
(106, '%8B', '<'),
(107, '%8C', 'O'),
(108, '%8E', 'Z'),
(109, '%91', '`'),
(110, '%92', '\''),
(111, '%95', ''),
(112, '%96', '-'),
(113, '%97', '-'),
(114, '%98', '~'),
(115, '%99', 'T'),
(116, '%9A', 's'),
(117, '%9B', '>'),
(118, '%9C', 'o'),
(119, '%9E', 'z'),
(120, '%9F', 'Y'),
(121, '%A1', '¡'),
(122, '%A2', 'ø'),
(123, '%A3', '£'),
(124, '%A4', ''),
(125, '%A5', 'Ø'),
(126, '%A6', '¦'),
(127, '%A7', ''),
(128, '%A9', 'c'),
(129, '%AA', 'ª'),
(130, '%AB', '«'),
(131, '%AC', '¬'),
(132, '%AE', 'r'),
(133, '%AF', '_'),
(134, '%B0', '°'),
(135, '%B1', '±'),
(136, '%B2', '²'),
(137, '%B3', '3'),
(138, '%B4', '\''),
(139, '%B5', 'µ'),
(140, '%B6', ''),
(141, '%B7', '·'),
(142, '%B8', ','),
(143, '%B9', '1'),
(144, '%BA', 'º'),
(145, '%BB', '»'),
(146, '%BC', '¼'),
(147, '%BD', '½'),
(148, '%BE', '_'),
(149, '%BF', '¿'),
(150, '%C0', 'A'),
(151, '%C1', 'A'),
(152, '%C2', 'A'),
(153, '%C3', 'A'),
(154, '%C4', 'Ä'),
(155, '%C5', 'Å'),
(156, '%C6', 'Æ'),
(157, '%C7', 'Ç'),
(158, '%C8', 'E'),
(159, '%C9', 'É'),
(160, '%CA', ''),
(161, '%CB', 'E'),
(162, '%CC', 'I'),
(163, '%CD', 'I'),
(164, '%CE', 'I'),
(165, '%CF', 'I'),
(166, '%D0', 'D'),
(167, '%D1', 'Ñ'),
(168, '%D2', 'O'),
(169, '%D3', 'O'),
(170, '%D4', 'O'),
(171, '%D5', 'O'),
(172, '%D6', 'Ö'),
(173, '%D7', 'x'),
(174, '%D8', 'O'),
(175, '%D9', 'U'),
(176, '%DA', 'U'),
(177, '%DB', 'U'),
(178, '%DC', 'Ü'),
(179, '%DD', 'Y'),
(180, '%DE', '_'),
(181, '%DF', 'ß'),
(182, '%E0', 'à'),
(183, '%E1', 'á'),
(184, '%E2', 'â'),
(185, '%E3', 'a'),
(186, '%E4', 'ä'),
(187, '%E5', 'å'),
(188, '%E6', 'æ'),
(189, '%E7', 'ç'),
(190, '%E8', 'è'),
(191, '%E9', 'é'),
(192, '%EA', 'ê'),
(193, '%EB', 'ë'),
(194, '%EC', 'ì'),
(195, '%ED', 'í'),
(196, '%EE', 'î'),
(197, '%EF', 'ï'),
(198, '%F0', 'd'),
(199, '%F1', 'ñ'),
(200, '%F2', 'ò'),
(201, '%F3', 'ó'),
(202, '%F4', 'ô'),
(203, '%F5', 'o'),
(204, '%F6', 'ö'),
(205, '%F7', '÷'),
(206, '%F8', 'o'),
(207, '%F9', 'ù'),
(208, '%FA', 'ú'),
(209, '%FB', 'û'),
(210, '%FC', 'ü'),
(211, '%FD', 'y'),
(212, '%FE', '_'),
(213, '%FF', 'ÿ');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(255) NOT NULL,
  `username` varchar(255) CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL,
  `password` varchar(255) CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'user1', 'password');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `gifts`
--
ALTER TABLE `gifts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `urlcodemap`
--
ALTER TABLE `urlcodemap`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `urlcodemapUIdx1` (`encoded`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `gifts`
--
ALTER TABLE `gifts`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `urlcodemap`
--
ALTER TABLE `urlcodemap`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=214;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
