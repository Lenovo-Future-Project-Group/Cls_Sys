-- Active: 1666235150193@@101.43.61.66@3306@cls_sys
-- 一、 创建数据库：cls_sys
create database if not exists cls_sys default character set 'utf8';
-- ----------------------------------------------------------------------------------

-- 二、 创建表：

-- 1.1 考勤系统：系室表，班级表，学生表，课程表，考勤记录表, 说明表，配置表
-- 1.1.1 系室表 cls_sys_department
create table if not exists cls_sys_department
(
    id          varchar(64) not null primary key comment '使用md5加密的系室ID',
    name        varchar(32) not null comment '系室名称',
    teacher     varchar(20) not null comment '系室负责人',
    create_time timestamp   not null default CURRENT_TIMESTAMP comment '创建时间',
    update_time timestamp   not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default charset = utf8 comment '系室表';

-- 1.1.2 班级表 cls_class
create table if not exists cls_class
(
    id          varchar(64) not null primary key comment '使用md5加密的班级ID',
    name        varchar(32) not null comment '班级名称',
    teacher     varchar(20) not null comment '班级负责人',
    create_time timestamp   not null default CURRENT_TIMESTAMP comment '创建时间',
    update_time timestamp   not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default charset = utf8 comment '班级表';

-- 1.1.3 学生表 cls_student
create table if not exists cls_student
(
    id     varchar(64) not null primary key comment '使用md5加密的学生ID',
    name   varchar(32) not null comment '姓名',
    age    tinyint     not null default 18 comment '年龄',
    info   varchar(64) not null default '{null}' comment '学生信息',
    gender tinyint     not null default 1 comment '性别：1男生，2女生'
) default charset = utf8 comment '学生表';


-- 1.1.4 课程表 cls_course
create table if not exists cls_course
(
    id          varchar(64) not null primary key comment '使用md5加密的课程ID',
    name        varchar(32) not null comment '课程名称',
    teacher     varchar(20) not null comment '任课老师',
    create_time timestamp   not null default CURRENT_TIMESTAMP comment '创建时间',
    update_time timestamp   not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default charset = utf8 comment '课程表';

-- 1.1.5 考勤记录表 cls_attendance
create table if not exists cls_attendance
(
    id          varchar(64) not null primary key comment '使用md5加密的考勤记录ID',
    student_id  varchar(64) not null comment '学生id',
    course_id   varchar(64) not null comment '课程id',
    status      tinyint     not null default 1 comment '考勤状态：1正常，2迟到，3早退，4旷课',
    create_time timestamp   not null default CURRENT_TIMESTAMP comment '创建时间',
    update_time timestamp   not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default charset = utf8 comment '考勤记录表';

-- 1.1.6 说明表 cls_explain
create table if not exists cls_explain
(
    id          varchar(64) not null primary key comment '使用md5加密的说明ID',
    name        varchar(32) not null comment '说明名称',
    content     varchar(64) not null comment '说明内容',
    create_time timestamp   not null default CURRENT_TIMESTAMP comment '创建时间',
    update_time timestamp   not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default charset = utf8 comment '说明表';

-- 1.1.7 配置表 cls_config
create table if not exists cls_config
(
    id          varchar(64) not null primary key comment '使用md5加密的配置ID',
    name        varchar(32) not null comment '配置名称',
    content     varchar(64) not null comment '配置内容',
    create_time timestamp   not null default CURRENT_TIMESTAMP comment '创建时间',
    update_time timestamp   not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default charset = utf8 comment '配置表';