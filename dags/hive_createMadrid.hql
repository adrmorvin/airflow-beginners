CREATE DATABASE adr_madrid;
use adr_madrid;

CREATE TABLE padron(
COD_DISTRITO string,
DESC_DISTRITO string,
COD_DIST_BARRIO string,
DESC_BARRIO string,
COD_BARRIO string,
COD_DIST_SECCION string,
COD_SECCION string,
COD_EDAD_INT string,
EspanolesHombres string,
EspanolesMujeres string,
ExtranjerosHombres string,
ExtranjerosMujeres string
)  
ROW FORMAT DELIMITED 
fields terminated by ';'
LOCATION
  '/user/hadoop/data/padronMadrid.txt'

