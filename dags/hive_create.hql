CREATE DATABASE adr_library;
use adr_library;

CREATE TABLE players(
id int, 
player_name string ,
country string,
salary int
)  
ROW FORMAT DELIMITED 
fields terminated by ','
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE TABLE teams(
id int, 
team_name string 
)  
ROW FORMAT DELIMITED 
fields terminated by ','
TBLPROPERTIES ("skip.header.line.count"="1");

