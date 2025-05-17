-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 17, 2025 at 02:15 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `breed`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `accountid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`accountid`, `name`, `username`, `password`) VALUES
(1, 'admin', 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `pet`
--

CREATE TABLE `pet` (
  `petID` int(11) NOT NULL,
  `petname` varchar(100) NOT NULL,
  `gender` varchar(100) NOT NULL,
  `age` int(100) NOT NULL,
  `species` varchar(100) NOT NULL,
  `owner` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `contact` int(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `allergies` varchar(255) NOT NULL,
  `vaccine` int(11) NOT NULL,
  `tvaccine` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pet`
--

INSERT INTO `pet` (`petID`, `petname`, `gender`, `age`, `species`, `owner`, `address`, `contact`, `status`, `allergies`, `vaccine`, `tvaccine`) VALUES
(2, 'guko', 'male', 5, 'cat', 'popoy', 'palkan', 934567, 'Adopted', 'egg', 2, 'Deworm'),
(3, 'Gohan', 'Male', 2, 'lizard', 'Spiderman', 'PolMargen', 2147483647, 'Adopted', 'gulay', 2, 'Deworm'),
(5, 'naruto', 'Female', 2, 'Dog', 'popoy', 'palkan', 2147483647, 'Adopted', '', 0, ''),
(6, 'Piccolo', 'Female', 3, 'Dog', 'gelloyd', 'Palkan', 96767673, 'Adopted', '', 0, ''),
(7, 'Luffy', 'male', 3, 'dog', 'nikus', 'tinio', 976543456, 'Adopted', '3', 1, 'deworm'),
(8, 'guko', 'male', 1, 'dog', 'popoy', 'palkan', 934567, 'Adopted', '', 0, ''),
(9, 'petpet', 'male', 2, 'dog', '', '', 0, 'available', '', 0, ''),
(10, 'sky', 'female', 1, 'cat', '', '', 0, 'available', '', 0, ''),
(11, 'terter', 'male', 2, 'cat', 'popoy', 'palkan', 945678, 'Adopted', 'bulad', 2, 'parvo');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`accountid`);

--
-- Indexes for table `pet`
--
ALTER TABLE `pet`
  ADD PRIMARY KEY (`petID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `accountid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `pet`
--
ALTER TABLE `pet`
  MODIFY `petID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
