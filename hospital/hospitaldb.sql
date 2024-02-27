
CREATE DATABASE IF NOT EXISTS `hospitaldb`
USE `hospitaldb`;

CREATE TABLE IF NOT EXISTS `Consulta` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `cantPacientes` int(10) unsigned NOT NULL,
  `nombreEspecialista` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `tipoConsulta` int(10) unsigned NOT NULL,
  `estado` enum('Ocupada','Disponible') CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_Consulta_tipoConsulta` (`tipoConsulta`),
  CONSTRAINT `FK_Consulta_tipoConsulta` FOREIGN KEY (`tipoConsulta`) REFERENCES `TipoConsulta` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Consulta` (`ID`, `cantPacientes`, `nombreEspecialista`, `tipoConsulta`, `estado`) VALUES
	(1, 0, 'Alberto Camus', 1, 'Ocupada'),
	(2, 0, 'Juan Mora', 3, 'Ocupada'),
	(3, 0, 'Pedro Sepulveda', 2, 'Ocupada'),
	(4, 1, 'Marta Gonzalez', 1, 'Ocupada'),
	(5, 0, 'Martin Parra', 2, 'Ocupada'),
	(6, 1, 'Katherine Baeza', 3, 'Ocupada');



CREATE TABLE IF NOT EXISTS `Hospital` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Hospital` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `IDConsulta` int(10) unsigned NOT NULL,
  `IDPaciente` int(10) unsigned NOT NULL,
  `registrofecha` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`ID`),
  KEY `FK_Hospital_consulta` (`IDConsulta`),
  KEY `FK_Hospital_paciente` (`IDPaciente`),
  CONSTRAINT `FK_Hospital_consulta` FOREIGN KEY (`IDConsulta`) REFERENCES `Consulta` (`ID`),
  CONSTRAINT `FK_Hospital_paciente` FOREIGN KEY (`IDPaciente`) REFERENCES `Paciente` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS `Paciente` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `edad` int(11) NOT NULL DEFAULT 0,
  `noHistoriaClinica` int(11) NOT NULL,
  `fechaNac` date DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Paciente` (`ID`, `nombre`, `edad`, `noHistoriaClinica`, `fechaNac`) VALUES
	(1, 'Juan Perez', 27, 10021, '1996-05-27'),
	(2, 'Miguel Pinto', 62, 201, '1961-06-18'),
	(3, 'Benjamin  Molina', 7, 25663, '2016-11-02'),
	(5, 'Esteban Peronni', 30, 52145, '1994-01-06'),
	(7, 'Marco Aurelio DosSantos', 25, 53596, '1999-10-05');

CREATE TABLE IF NOT EXISTS `PAnciano` (
  `ID` int(11) unsigned NOT NULL,
  `tieneDieta` tinyint(4) NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `FK_PAnciano_ID` FOREIGN KEY (`ID`) REFERENCES `Paciente` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `PAnciano` (`ID`, `tieneDieta`) VALUES
	(2, 0);

CREATE TABLE IF NOT EXISTS `PJoven` (
  `ID` int(10) unsigned NOT NULL,
  `fumador` tinyint(4) NOT NULL DEFAULT 0,
  `fumaDesde` mediumint(8) unsigned DEFAULT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `FK_PJoven_ID` FOREIGN KEY (`ID`) REFERENCES `Paciente` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `PJoven` (`ID`, `fumador`, `fumaDesde`) VALUES
	(1, 1, 2020),
	(5, 1, 2010),
	(7, 0, NULL);

CREATE TABLE IF NOT EXISTS `PNinno` (
  `ID` int(10) unsigned NOT NULL,
  `relacionPesoEstatura` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `FK_PNinno_ID` FOREIGN KEY (`ID`) REFERENCES `Paciente` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `PNinno` (`ID`, `relacionPesoEstatura`) VALUES
	(3, 2);

CREATE TABLE IF NOT EXISTS `SalaEspera` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `IDPaciente` int(10) unsigned NOT NULL,
  `estado` tinyint(3) unsigned NOT NULL DEFAULT 1,
  `registrofecha` datetime NOT NULL DEFAULT current_timestamp(),
  `prioridad` float NOT NULL DEFAULT 0,
  `riesgo` float NOT NULL DEFAULT 0,
  `llegada` datetime NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_Salaespera_paciente` (`IDPaciente`),
  CONSTRAINT `FK_Salaespera_paciente` FOREIGN KEY (`IDPaciente`) REFERENCES `Paciente` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS `SalaPendiente` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `IDPaciente` int(10) unsigned NOT NULL,
  `estado` tinyint(4) NOT NULL DEFAULT 1,
  `llegada` datetime NOT NULL DEFAULT current_timestamp(),
  `prioridad` float NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_Salapendiente_Paciente` (`IDPaciente`),
  CONSTRAINT `FK_Salapendiente_Paciente` FOREIGN KEY (`IDPaciente`) REFERENCES `Paciente` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS `TipoConsulta` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `descripcion` varchar(150) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `TipoConsulta` (`ID`, `nombre`, `descripcion`) VALUES
	(1, 'Pediatria', 'Atención a menores de 15 años'),
	(2, 'Urgencias', 'Atención a pacientes de alto riesgo'),
	(3, 'CGI', 'Consulta General Integral');
