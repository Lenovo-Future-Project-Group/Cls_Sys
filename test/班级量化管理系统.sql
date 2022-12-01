-- Active: 1666235150193@@101.43.61.66@3306@cls_sys
-- 一、 创建数据库：cls_sys
create database if not exists pear_admin_flask default character set "utf8";
use cls_sys;
-- ----------------------------------------------------------------------------------

-- 2.1 量化系统：班主任表、系主任表、检查员表
-- ----------------------------------------------------------------------------------

-- 二、 创建表：
-- 2.1 人员表 user
drop table if exists user;
create table if not exists user(
    id         varchar(64) not null primary key comment '对姓名使用md5加密的id',
    name        varchar(32) not null comment '姓名',
    username    varchar(128) not null comment '登陆的邮箱',
    password    varchar(128) not null comment '登陆的密码',
    is_headdepart   tinyint not null default 0 comment '是不是系主任',
    is_inspector    tinyint not null default 0 comment '是不是检查员',
    is_headteacher  tinyint not null default 0 comment '是不是班主任',
    depart      varchar(32) default '信息技术' comment '院系',
    permission_level    tinyint not null default 1 comment '权限等级:1级、2级、3级、4级,4级最高',
    token       varchar(32) comment 'token'
) comment '人员表' collate = utf8_unicode_ci;

-- 2.2 创建检查表：检查的班级、检查项目的分类
-- 2.2.1 需要检查的班级 inspect_class
drop table if exists inspect_class;
create table if not exists inspect_class(
    id          int         not null primary key auto_increment comment 'id',
    cls         varchar(32) not null comment '班级',
    grade       varchar(32) comment '年级',
    depart      varchar(32) default '信息技术' comment '院系',
    user_id     tinyint not null comment '对应的user表中的班主任id'
) comment '班级表' collate = utf8_unicode_ci;

-- 2.2.2 检查项目表：教室、宿舍、个人卫生、楼值、纪律等
drop table if exists inspect_items;
create table if not exists inspect_items(
    id          int not null primary key auto_increment comment 'id',
    category    varchar(32) comment "检查的大类，如：教室、宿舍、个人卫生、楼值、纪律等",
    item        varchar(64) comment "大类下的细分项，如：教室卫生、教室桌椅的摆放、宿舍的床铺等",
    score       int comment "分值",
    create_time    timestamp   not null default CURRENT_TIMESTAMP comment '创建时间'
) comment '检查项目表' collate = utf8_unicode_ci;

-- 2.2.3 检查结果表 inspect_result
drop table if exists inspect_result;
create table if not exists inspect_result(
    id          int             not null primary key auto_increment comment 'id',
    cls         varchar(32)     not null comment '班级',
    classroom   varchar(512)    default '{\'分数\':100}' comment '教室',
    dormitory   varchar(512)    default '{\'分数\':100}' comment '宿舍',
    personal    varchar(512)    default '{\'分数\':100}' comment '个人卫生',
    floor       varchar(512)    default '{\'分数\':100}' comment '楼值',
    discipline  varchar(512)    default '{\'分数\':100}' comment '纪律',
    user_id     tinyint not null comment '对应user表中的班主任id',
    inspector_id    tinyint not null comment '对应user表中的检查员姓名',
    inspect_time       datetime    default now() comment '检查时间'
) comment '检查结果表' collate = utf8_unicode_ci;

-- ------------------------------------------------------------------------------------

-- 3 插入数据
-- 3.1 班级表
insert into inspect_class(`cls`,`grade`,`user_id`)
values
('1班','2020级',1),
('2班','2020级',2),
('1班','2021级',3);

-- 3.2 人员表
insert into user(`id`,`name`,`username`,`password`,`is_headdepart`,`is_inspector`,`is_headteacher`,`permission_level`)
values
('1','邢予','xingyu@qq.com','xingyu321',0,1,1,2),
('2','吴洁','wujie@qq.com','wujie321',0,1,1,2),
('3','王钰坤','wangyukun@qq.com','wangyukun321',0,0,1,1),
('4','陕娟娟','shanjuanjuan@qq.com','shanjuanjuan321',0,1,0,3),
('5','王璐','wanglu@qq.com','wanglu321',1,1,0,3),
('6','赵东','zhaodong@qq.com','zhaodong321',1,0,0,3),
('7','方荣卫','fangrongwei@qq.com','fangrongwei321',1,0,0,3),
('8','demo','demo@qq.com','demo',1,0,0,4);

-- 3.3 检查项目表
insert into inspect_items(`category`,`item`,`score`)
values
("classroom","黑板",10),
("classroom","桌椅",10),
("classroom","水杯",10),
("classroom","地面卫生",10),
("classroom","灯",10),
("classroom","门窗",10),
("classroom","垃圾",10),
("classroom","其他",10),
("dormitory","床铺",10),
("dormitory","衣物",10),
("dormitory","门窗",10),
("dormitory","垃圾",10),
("dormitory","其他",10),
("personal","发型",10),
("personal","指甲",10),
("personal","饰品",10),
("personal","其他",10),
("floor","卫生间",10),
("floor","楼道",10),
("floor","其他",10),
("discipline","上课讲话",10),
("discipline","上课睡觉",10),
("discipline","上课玩手机",10),
("discipline","其他",10);

-- 检查结果表
insert into inspect_result(`cls`,`user_id`,`inspector_id`,`classroom`,`dormitory`,`personal`,`floor`,`discipline`)
  values
  ("大数据201",1,3,'{"分数":80,"减分项":{"纸屑":10,"黑板":10}}','{"分数":80,"减分项":{"床铺":10,"衣物叠放":10}}','{"分数":80,"减分项":{"指甲":10,"头发":10}}','{"分数":80,"减分项":{"地面":10,"垃圾桶":10}}','{"分数":80,"减分项":{"上课打闹":10,"玩手机":10}}'),
  ("大数据201",4,3,'{"分数":80,"减分项":{"纸屑":10,"黑板":10}}','{"分数":80,"减分项":{"床铺":10,"衣物叠放":10}}','{"分数":80,"减分项":{"指甲":10,"头发":10}}','{"分数":80,"减分项":{"地面":10,"垃圾桶":10}}','{"分数":80,"减分项":{"上课打闹":10,"玩手机":10}}'),
  ("大数据201",2,4,'{"分数":80,"减分项":{"纸屑":10,"黑板":10}}','{"分数":80,"减分项":{"床铺":10,"衣物叠放":10}}','{"分数":80,"减分项":{"指甲":10,"头发":10}}','{"分数":80,"减分项":{"地面":10,"垃圾桶":10}}','{"分数":80,"减分项":{"上课打闹":10,"玩手机":10}}'),
  ("大数据201",5,1,'{"分数":80,"减分项":{"纸屑":10,"黑板":10}}','{"分数":80,"减分项":{"床铺":10,"衣物叠放":10}}','{"分数":80,"减分项":{"指甲":10,"头发":10}}','{"分数":80,"减分项":{"地面":10,"垃圾桶":10}}','{"分数":80,"减分项":{"上课打闹":10,"玩手机":10}}'),
  ("大数据201",3,6,'{"分数":80,"减分项":{"纸屑":10,"黑板":10}}','{"分数":80,"减分项":{"床铺":10,"衣物叠放":10}}','{"分数":80,"减分项":{"指甲":10,"头发":10}}','{"分数":80,"减分项":{"地面":10,"垃圾桶":10}}','{"分数":80,"减分项":{"上课打闹":10,"玩手机":10}}');
