-- Active: 1666235150193@@101.43.61.66@3306@cls_sys
-- 一、 创建数据库：cls_sys
create database if not exists cls_sys default character set 'utf8';
-- ----------------------------------------------------------------------------------

-- 二、 创建表：

-- 1.1 考勤系统：学生表，考勤表，课程表
-- 1.1.1 学生表 cls_student
create table if not exists cls_student
(
    sid         int(16)     not null primary key auto_increment comment '学生ID 唯一主键',
    sage        int(03)     not null default 18 comment '学生年龄',
    ssex        int(02)     not null default 00 comment '学生性别， 0：男， 1：女',
    sname       varchar(32) not null comment '学生姓名',
    create_time timestamp   not null default CURRENT_TIMESTAMP comment '创建时间',
    update_time timestamp   not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default charset = utf8 comment '学生表';

-- 1.1.2 考勤表 cls_attendance
create table if not exists cls_attendance
(
    sid             int(16)     not null comment '学生ID',
    cid             int(16)     not null comment '班级ID',
    attendance_info varchar(32) not null default '0' comment '学生考勤信息: 0：正常， 1：迟到， 2：早退， 3：旷课',
    create_time     timestamp   not null default CURRENT_TIMESTAMP comment '创建时间',
    update_time     timestamp   not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default charset = utf8 comment '考勤表';

-- 1.1.3 课程表 cls_course
create table if not exists cls_course
(
    cid         int(16)     not null primary key auto_increment comment '课程ID',
    cname       varchar(32) not null comment '课程名称',
    create_time timestamp   not null default CURRENT_TIMESTAMP comment '创建时间',
    update_time timestamp   not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default charset = utf8 comment '课程表';

alter table cls_attendance
    add constraint fk_sid foreign key (sid) references cls_student (sid);

alter table cls_attendance
    add constraint fk_cid foreign key (cid) references cls_course (cid);