-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 03. Mrz 2026 um 08:30
-- Server-Version: 10.4.32-MariaDB
-- PHP-Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `projekt-verein`
--
CREATE DATABASE IF NOT EXISTS `projekt-verein` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `projekt-verein`;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `abteilungen`
--

CREATE TABLE IF NOT EXISTS `abteilungen` (
  `ID_Abteilung` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  PRIMARY KEY (`ID_Abteilung`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `abteilungen`
--

INSERT INTO `abteilungen` (`ID_Abteilung`, `Name`) VALUES
(1, 'Fußball'),
(2, 'Handball'),
(3, 'Tennis');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `kommentare`
--

CREATE TABLE IF NOT EXISTS `kommentare` (
  `ID_Kommentar` int(11) NOT NULL,
  `ID_Spiel` int(11) NOT NULL,
  `Autor` varchar(100) NOT NULL,
  `Text` varchar(250) NOT NULL,
  PRIMARY KEY (`ID_Kommentar`),
  KEY `ID_Spiel` (`ID_Spiel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ligen`
--

CREATE TABLE IF NOT EXISTS `ligen` (
  `ID_Liga` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Saison` varchar(20) NOT NULL,
  PRIMARY KEY (`ID_Liga`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `ligen`
--

INSERT INTO `ligen` (`ID_Liga`, `Name`, `Saison`) VALUES
(1, 'Bezirksmittelliga Fußball', '2025/2026'),
(2, 'Kreisoberliga Handball', '2025/2026'),
(3, 'Wimbledon Tennis', '2026');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `reaktionen`
--

CREATE TABLE IF NOT EXISTS `reaktionen` (
  `ID_Reaktion` int(11) NOT NULL,
  `ID_Spiel` int(11) NOT NULL,
  `Emoji` varchar(10) NOT NULL,
  PRIMARY KEY (`ID_Reaktion`),
  KEY `ID_Spiel` (`ID_Spiel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `spiele`
--

CREATE TABLE IF NOT EXISTS `spiele` (
  `ID_Abteilung` int(11) NOT NULL,
  `ID_Spiel` int(11) NOT NULL,
  `ID_Liga` int(11) NOT NULL,
  `ID_Heimverein` int(11) NOT NULL,
  `ID_Gastverein` int(11) NOT NULL,
  `Datum` date NOT NULL,
  `Status` varchar(20) NOT NULL,
  `Tore_Heim` int(11) NOT NULL,
  `Tore_Gast` int(11) NOT NULL,
  PRIMARY KEY (`ID_Spiel`),
  KEY `ID_Liga` (`ID_Liga`),
  KEY `ID_Abteilung` (`ID_Abteilung`),
  KEY `ID_Heimverein` (`ID_Heimverein`),
  KEY `ID_Gastverein` (`ID_Gastverein`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `spiele`
--

INSERT INTO `spiele` (`ID_Abteilung`, `ID_Spiel`, `ID_Liga`, `ID_Heimverein`, `ID_Gastverein`, `Datum`, `Status`, `Tore_Heim`, `Tore_Gast`) VALUES
(1, 1, 1, 1, 2, '2026-03-20', 'geplant', 0, 0),
(1, 2, 1, 2, 1, '2026-03-27', 'geplant', 0, 0);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `vereine`
--

CREATE TABLE IF NOT EXISTS `vereine` (
  `ID_Verein` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `ist_heimverein` tinyint(1) NOT NULL,
  PRIMARY KEY (`ID_Verein`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `vereine`
--

INSERT INTO `vereine` (`ID_Verein`, `Name`, `ist_heimverein`) VALUES
(1, 'TS Herzo', 1),
(2, 'FC Rasenmäher', 0),
(3, 'SV Hopfenblüte', 0);

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `kommentare`
--
ALTER TABLE `kommentare`
  ADD CONSTRAINT `kommentare_ibfk_1` FOREIGN KEY (`ID_Spiel`) REFERENCES `spiele` (`ID_Spiel`);

--
-- Constraints der Tabelle `reaktionen`
--
ALTER TABLE `reaktionen`
  ADD CONSTRAINT `reaktionen_ibfk_1` FOREIGN KEY (`ID_Spiel`) REFERENCES `spiele` (`ID_Spiel`);

--
-- Constraints der Tabelle `spiele`
--
ALTER TABLE `spiele`
  ADD CONSTRAINT `spiele_ibfk_1` FOREIGN KEY (`ID_Liga`) REFERENCES `ligen` (`ID_Liga`),
  ADD CONSTRAINT `spiele_ibfk_2` FOREIGN KEY (`ID_Abteilung`) REFERENCES `abteilungen` (`ID_Abteilung`),
  ADD CONSTRAINT `spiele_ibfk_3` FOREIGN KEY (`ID_Heimverein`) REFERENCES `vereine` (`ID_Verein`),
  ADD CONSTRAINT `spiele_ibfk_4` FOREIGN KEY (`ID_Gastverein`) REFERENCES `vereine` (`ID_Verein`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
