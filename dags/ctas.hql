CREATE TABLE padron2 
    row format delimited 
    fields terminated by ';' 
    STORED AS PARQUET 
AS select * from padron