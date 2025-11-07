<<<<<<< HEAD
create database gzf;

=======
>>>>>>> c4ba579a8612b4f108b5dbfd52860c8932752113
drop table `HouseData`;
CREATE TABLE `HouseData` (
   `house_id` INT UNSIGNED AUTO_INCREMENT  comment '自增主键',
   `house_name` varchar(512) COLLATE utf8_bin NOT NULL DEFAULT '' comment '房屋名称',
   `house_site` varchar(512) COLLATE utf8_bin NOT NULL DEFAULT '' comment '房屋位置',
   `rent_monoey` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '' comment '租金',
   `choose_start_time` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '' comment '选房开始时间',
   `choose_end_time` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '' comment '选房结束时间',
   `house_type` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '' comment '房型',
   `choosed` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '' comment '已选',
   `foold` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '' comment '楼层',
   `area` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '' comment '面积',
   `last_update_date` datetime default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
   PRIMARY KEY (`house_id`,`last_update_date`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='公租房';
 
INSERT into HouseData 
      (house_name,house_site,rent_monoey,choose_start_time,choose_end_time,house_type,choosed,foold,area) 
  VALUES
    (house_name,house_site,rent_monoey,choose_start_time,choose_end_time,house_type,choosed,foold,area);

 show create table HouseData;
 
 select * from HouseData;
 
 INSERT INTO HouseData(house_id,get_time,house_source)values ('','2022-11-30 23:22:25','民生路318弄(馨澜公寓)/01号/11楼/1101');
 
 INSERT INTO HouseData(house_name)values ('民生路318弄(馨澜公寓)/01号/21楼/2101')