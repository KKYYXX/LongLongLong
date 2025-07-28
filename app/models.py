
from app.plugins import db
from datetime import datetime

#创建模型

class Projects15(db.Model):
    """
    "双百行动"校地合作共建项目清单(2025年) 模型
    """
    __tablename__ = '15projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='项目唯一标识')
    serial_number = db.Column(db.Numeric(10, 0), comment='项目序号')
    city = db.Column(db.String(50), nullable=False, comment='项目所在地级市')
    county = db.Column(db.String(50), nullable=False, comment='结对县(市、区)')
    universities = db.Column(db.Text, nullable=False, comment='组团结对高校院所，多个高校用换行分隔')
    project_name = db.Column(db.String(200), nullable=False, comment='项目名称')
    implementing_institutions = db.Column(db.Text, nullable=False, comment='项目实施单位(高校院所)，多个单位用换行分隔')
    is_key_project = db.Column(db.Enum('是', '否'), nullable=False, comment='是否重点项目')
    involved_areas = db.Column(db.Text, comment='涉及典型县镇村，多个地区用换行分隔')
    project_type = db.Column(db.Enum(
        '强化产业发展科技支撑',
        '强化城乡规划建设服务',
        '突出基本公共服务支持',
        '突出基层人才培养培训',
        '参与集体经济运营',
        '参与基层改革创新探索',
        '提供决策咨询服务'
    ), nullable=False, comment='项目类型')
    start_date = db.Column(db.String(7), nullable=False, comment='项目开始时间（年月）')
    end_date = db.Column(db.String(7), nullable=False, comment='项目结束时间（年月）')
    background = db.Column(db.Text, comment='项目背景')
    content_and_measures = db.Column(db.Text, comment='项目内容和落实的具体举措')
    objectives = db.Column(db.Text, comment='主要任务目标(量化指标)')
    contacts = db.Column(db.Text, comment='联系人(职务)和联系方式')
    remarks = db.Column(db.Text, comment='备注')

    def __repr__(self):
        return f'<Project15 {self.id}: {self.project_name}>'


class UserModel(db.Model):
    """
    小程序用户账户表模型
    """
    __tablename__ = 'users'

    name = db.Column(db.String(50), nullable=False, comment='用户真实姓名')
    phone = db.Column(db.String(20), primary_key=True, unique=True, comment='用户手机号（唯一）')
    password = db.Column(db.String(255), nullable=False, comment='加密后的用户密码')
    wx_openid = db.Column(db.String(128), comment='微信openid')
    principal = db.Column(db.Boolean, default=False, comment='1表true，0表false，默认为0')
    alter_15 = db.Column(db.Boolean, default=False, comment='1表true，0表false，默认为0')
    query_15 = db.Column(db.Boolean, default=False, comment='1表true，0表false，默认为0')
    alter_zc = db.Column(db.Boolean, default=False, comment='1表true，0表false，默认为0')
    alter_model = db.Column(db.Boolean, default=False, comment='1表true，0表false，默认为0')

    def __repr__(self):
        return f'<User {self.phone}: {self.name}>'


class UploadModel(db.Model):
    """
    用户上传文件信息表模型
    """
    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增主键ID')
    user_id = db.Column(db.String(128), nullable=False, comment='微信用户唯一标识openid')
    file_name = db.Column(db.String(255), nullable=False, comment='用户上传的原始文件名')
    file_type = db.Column(db.Enum('pdf', 'doc', 'docx'), nullable=False, comment='文件类型(pdf/word)')
    file_size = db.Column(db.Integer, nullable=False, comment='文件大小(单位：字节)')
    file_url = db.Column(db.String(512), nullable=False, comment='完整的文件访问URL地址')
    has_text = db.Column(db.Boolean, nullable=False, default=True, comment='标记文件是否包含文字')
    has_images = db.Column(db.Boolean, nullable=False, default=False, comment='标记文件是否包含图片')
    video_url = db.Column(db.String(512), comment='关联视频文件URL（可选）')
    upload_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='文件上传时间')
    status = db.Column(db.Enum('pending', 'processed', 'failed'), default='pending', comment='文件处理状态')

    def __repr__(self):
        return f'<UploadModel {self.id}: {self.file_name}>'


class ZCDocument(db.Model):
    """
    用户上传文档记录表(PDF/Word)模型
    """
    __tablename__ = 'zc_documents'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='文档唯一标识ID')
    user_id = db.Column(db.String(128), nullable=False, comment='微信用户openid')
    file_url = db.Column(db.String(512), nullable=False, comment='文件访问URL')
    file_type = db.Column(db.Enum('pdf', 'doc', 'docx'), nullable=False, comment='文件类型(pdf/word)')
    original_name = db.Column(db.String(255), nullable=False, comment='原始文件名')
    file_size = db.Column(db.Integer, nullable=False, comment='文件大小(字节)')
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='上传时间')

    def __repr__(self):
        return f'<ZCDocument {self.id}: {self.original_name}>'


class TryModel(db.Model):
    """
    测试表 try 的模型
    """
    __tablename__ = 'try'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    name = db.Column(db.String(255), comment='名称字段')

    def __repr__(self):
        return f'<TryModel {self.id}: {self.name}>'


class TryZhigongModel(db.Model):
    """
    测试表 tryzhigong 的模型
    """
    __tablename__ = 'tryzhigong'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')

    def __repr__(self):
        return f'<TryZhigongModel {self.id}>'