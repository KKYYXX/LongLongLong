#放视图
from flask import Blueprint,request,jsonify,render_template
from app.models import TryModel,ZCDocument
from app.plugins import db
from sqlalchemy import func
from datetime import datetime

blue = Blueprint('blue',__name__)

#视图
'''
@blue.route('/dept/info/<id>',methods=['GET'])
#数据查询模型
def getDepInfo(id):

    dept= TryModel.query.get(id)

    return f'序号：{ dept.id }，名字：{ dept.name }'

#记录添加
@blue.route('/dept/add',methods=['POST'])
def addDepinfo():

    try1 = (TryModel(
    name = request.form.get('name'),
    id =request.form.get('id',type=int)
    ))
    db.session.add(try1)
    db.session.commit()

    return "添加信息成功"

#记录更新
@blue.route('/dept/upd',methods=['POST'])
def updDepinfo():

    try2 = TryModel.query.get(request.form.get('id'))
    try2.name = request.form.get('name')

    db.session.commit()

    return "修改信息成功"

#记录删除
@blue.route('/dept/del',methods=['POST'])
def delDepinfo():

    try3 = TryModel.query.get(request.form.get('id'))

    db.session.delete(try3)

    db.session.commit()

    return "删除信息成功"

#信息查询（条件查询）显示的是列表的形式
@blue.route('/dept/find',methods=['GET'])
def finddepts():

    info_1 = TryModel.query.filter(TryModel.name == '王五').first()  #只显示第一个查询结果

    #多条件查询
    info_2 = TryModel.query.filter(TryModel.name == '王五',TryModel.id == 3 ).all()  #显示所有查询结果

    return '查询成功'

#模糊查询
@blue.route('/dept/like',methods=['GET'])
def likedeptdatail():

    #            张%                 %三                %三%     都可
    # 分别对应 startswith('张')   endswith('三')     contains('三')
    info_1 = TryModel.query.filter(TryModel.name.like('张%')).all()

    result = []
    for item in info_1:
        result.append(f'序号：{item.id}，名字：{item.name}')
    return '\n'.join(result)

#模糊查询2.0
@blue.route('/dept/like1',methods=['GET'])
def like1deptdatail():

    info_1 = TryModel.query.filter(TryModel.name.startswith('张')).all()

    result = []
    for item in info_1:
        result.append(f'序号：{item.id}，名字：{item.name}')
    return '\n'.join(result)

#查询结果按升序排列显示，默认按升序
@blue.route('/dept/order',methods=['GET'])
def orderdeptdatail():

    info_1 = TryModel.query.order_by(TryModel.id).all()

    result = []
    for item in info_1:
        result.append(f'序号：{item.id}，名字：{item.name}')
    return '\n'.join(result)

#查询结果按降序排列显示
@blue.route('/dept/order1',methods=['GET'])
def order1deptdatail():

    info_1 = TryModel.query.order_by(TryModel.id.desc()).all()

    result = []
    for item in info_1:
        result.append(f'序号：{item.id}，名字：{item.name}')
    return '\n'.join(result)

#查询结果只显示前几条
@blue.route('/dept/top',methods=['GET'])
def topdeptdatail():

    #只看前两条
    info_1 = TryModel.query.limit(2).all()

    result = []
    for item in info_1:
        result.append(f'序号：{item.id}，名字：{item.name}')
    return '\n'.join(result)

#分组查询
@blue.route('/dept/group',methods=['GET'])
def groupdeptdatail():
    #按性别分组
    info = db.session\
        .query(TryModel.gender,func.count(TryModel.gender).label('count_gender'))\
        .group_by(TryModel.gender).all()

    result = []
    for item in info:
        result.append(f'性别：{item.gender}，数量：{item.count_gender}')
    return '\n'.join(result)
'''

# ==================== ZCDocument 表接口 ====================

# 测试页面路由
@blue.route('/zcdocuments_test', methods=['GET'])
def zcdocuments_test_page():
    """
    渲染ZCDocument测试页面
    """
    return render_template('zcdocuments_test.html')

# 1. 查询所有zc_documents数据
@blue.route('/api/zcdocuments', methods=['GET'])
def get_all_zcdocuments():
    """
    获取zc_documents表的所有数据
    返回JSON格式的数据列表
    """
    try:
        # 查询所有记录，按上传时间降序排列
        documents = ZCDocument.query.order_by(ZCDocument.uploaded_at.desc()).all()
        
        # 将查询结果转换为字典列表
        documents_list = []
        for doc in documents:
            documents_list.append({
                'user_id': doc.user_id,
                'file_url': doc.file_url,
                'file_type': doc.file_type,
                'original_name': doc.original_name,
                'file_size': doc.file_size,
                'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M:%S') if doc.uploaded_at else None
            })
        
        return jsonify({
            'success': True,
            'message': '查询成功',
            'data': documents_list,
            'total_count': len(documents_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'查询失败: {str(e)}',
            'data': []
        }), 500


# 2. 添加zc_documents数据
@blue.route('/api/zcdocuments', methods=['POST'])
def add_zcdocument():
    """
    添加新的zc_documents记录
    接收参数：
    - user_id: 微信用户openid
    - file_url: 文件访问URL
    - file_type: 文件类型(pdf/doc/docx)
    - original_name: 原始文件名
    - file_size: 文件大小(字节)
    """
    try:
        # 获取请求参数
        data = request.get_json() if request.is_json else request.form
        
        user_id = data.get('user_id')
        file_url = data.get('file_url')
        file_type = data.get('file_type')
        original_name = data.get('original_name')
        file_size = data.get('file_size')
        
        # 参数验证
        if not all([user_id, file_url, file_type, original_name, file_size]):
            return jsonify({
                'success': False,
                'message': '缺少必要参数：user_id, file_url, file_type, original_name, file_size'
            }), 400
        
        # 验证文件类型
        if file_type not in ['pdf', 'doc', 'docx']:
            return jsonify({
                'success': False,
                'message': '文件类型必须是 pdf, doc, 或 docx'
            }), 400
        
        # 验证文件大小是否为数字
        try:
            file_size = int(file_size)
            if file_size <= 0:
                raise ValueError("文件大小必须大于0")
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': '文件大小必须是正整数'
            }), 400
        
        # 创建新的ZCDocument记录
        new_document = ZCDocument(
            user_id=user_id,
            file_url=file_url,
            file_type=file_type,
            original_name=original_name,
            file_size=file_size,
            uploaded_at=datetime.utcnow()
        )
        
        # 添加到数据库
        db.session.add(new_document)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '添加成功',
            'data': {
                'id': new_document.id,
                'user_id': new_document.user_id,
                'file_url': new_document.file_url,
                'file_type': new_document.file_type,
                'original_name': new_document.original_name,
                'file_size': new_document.file_size,
                'uploaded_at': new_document.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'添加失败: {str(e)}'
        }), 500


# 3. 删除zc_documents记录
@blue.route('/api/zcdocuments/<int:document_id>', methods=['DELETE'])
def delete_zcdocument(document_id):
    """
    删除指定的zc_documents记录
    参数：document_id - 要删除的文档ID
    """
    try:
        # 查找要删除的记录
        document = ZCDocument.query.get(document_id)
        
        if not document:
            return jsonify({
                'success': False,
                'message': f'文档ID {document_id} 不存在'
            }), 404
        
        # 保存删除前的信息用于返回
        deleted_info = {
            'id': document.id,
            'original_name': document.original_name,
            'file_type': document.file_type
        }
        
        # 删除记录
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除成功',
            'deleted_document': deleted_info
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }), 500


# ==================== model 表接口 ====================

# 1. 查询所有model表记录
@blue.route('/api/models', methods=['GET'])
def get_all_models():
    """
    查询所有model表（用户上传文件信息表）记录
    """
    try:
        from app.models import UploadModel
        models = UploadModel.query.all()
        result = []
        for m in models:
            result.append({
                'id': m.id,
                'user_id': m.user_id,
                'file_name': m.file_name,
                'file_type': m.file_type,
                'file_size': m.file_size,
                'file_url': m.file_url,
                'has_text': m.has_text,
                'has_images': m.has_images,
                'video_url': m.video_url,
                'upload_time': m.upload_time.strftime('%Y-%m-%d %H:%M:%S') if m.upload_time else None,
            })
        return jsonify({'success': True, 'data': result}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'查询失败: {str(e)}'}), 500

# 2. 新增model表记录
@blue.route('/api/models', methods=['POST'])
def add_model():
    """
    新增一条model表记录
    """
    try:
        from app.models import UploadModel, db
        data = request.json
        user_id = data.get('user_id')
        file_name = data.get('file_name')
        file_type = data.get('file_type')
        file_size = data.get('file_size')
        file_url = data.get('file_url')
        has_text = data.get('has_text', True)
        has_images = data.get('has_images', False)
        video_url = data.get('video_url')
        # 校验必填
        if not all([user_id, file_name, file_type, file_size, file_url]):
            return jsonify({'success': False, 'message': '缺少必要参数'}), 400
        # 校验类型
        if file_type not in ['pdf', 'doc', 'docx']:
            return jsonify({'success': False, 'message': '文件类型必须是 pdf, doc, docx'}), 400
        try:
            file_size = int(file_size)
            if file_size <= 0:
                raise ValueError('文件大小必须大于0')
        except Exception:
            return jsonify({'success': False, 'message': '文件大小必须为正整数'}), 400
        new_model = UploadModel(
            user_id=user_id,
            file_name=file_name,
            file_type=file_type,
            file_size=file_size,
            file_url=file_url,
            has_text=bool(has_text),
            has_images=bool(has_images),
            video_url=video_url,
        )
        db.session.add(new_model)
        db.session.commit()
        return jsonify({'success': True, 'message': '添加成功', 'data': {'id': new_model.id}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'添加失败: {str(e)}'}), 500

# 3. 删除model表记录
@blue.route('/api/models/<int:model_id>', methods=['DELETE'])
def delete_model(model_id):
    """
    删除指定的model表记录
    参数：model_id - 要删除的记录ID
    """
    try:
        from app.models import UploadModel, db
        model = UploadModel.query.get(model_id)
        if not model:
            return jsonify({'success': False, 'message': f'记录ID {model_id} 不存在'}), 404
        db.session.delete(model)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功', 'deleted_id': model_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'}), 500


