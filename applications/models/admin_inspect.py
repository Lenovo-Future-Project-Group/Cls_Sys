import datetime
from applications.extensions import db



class InspectRes(db.Model):
    """ 检查结果 """
    __tablename__ = 'admin_inspect_result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    cls = db.Column(db.String(20), comment='班级')
    classroom = db.Column(db.String(128), comment='教室的扣分情况')
    dormitory = db.Column(db.String(128), comment='宿舍的扣分情况')
    personal = db.Column(db.String(128), comment='个人的扣分情况')
    floor = db.Column(db.String(128), comment='楼值的扣分情况')
    discipline = db.Column(db.String(128), comment='纪律的扣分情况')
    head_teacher = db.Column(db.String(20), comment='班主任')
    inspector = db.Column(db.String(20), comment='督察员')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')



# class InspectCls(db.Model):
#     """ 检查的班级 """
#     __tablename__ = 'admin_inspect_cls'
    
    