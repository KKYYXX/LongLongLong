#放视图
from flask import Blueprint,request,jsonify,render_template
from app.models import TryModel,ZCDocument
from app.plugins import db
from sqlalchemy import func
from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from app.models import TryModel, UserModel, ZCDocument, UploadModel

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

# ==================== UserModel 表接口 ====================
#用户注册接口（返回姓名、号码、微信、密码）
@blue.route('/user/register', methods=['POST'])
def register_user():
    # 获取请求中的注册信息
    name = request.form.get('name')
    phone = request.form.get('phone')
    password = request.form.get('password')
    wx_openid = request.form.get('wx_openid')

    # 查询手机号是否已经注册
    existing_user = UserModel.query.filter_by(phone=phone).first()

    if existing_user:
        # 如果用户已存在，匹配名字和微信号
        if existing_user.name == name and existing_user.wx_openid == wx_openid:
            # 如果匹配，允许注册（返回用户信息）
            user_info = {
                'name': existing_user.name,
                'phone': existing_user.phone,
                'wx_openid': existing_user.wx_openid,
                'password': existing_user.password  # Assuming password is already hashed
            }
            return jsonify(user_info), 200  # Registration successful (user exists and matches)
        else:
            # 如果名字和微信号不匹配，注册失败
            return jsonify({'message': 'User details do not match'}), 400
    else:
        # 如果用户不存在
        return jsonify({'message': 'User not found'}), 404

#转让页面接口（返回姓名、号码、密码）
@blue.route('/user/validate', methods=['POST'])
def validate_user():
    # 获取请求中的数据
    name = request.form.get('name')
    phone = request.form.get('phone')
    password = request.form.get('password')

    # 查询数据库中是否有该用户
    user = UserModel.query.filter_by(phone=phone).first()

    if user:
        # 如果用户存在，验证姓名和密码
        if user.name == name and check_password_hash(user.password, password):
            # 如果姓名和密码匹配，更新principal字段为True
            user.principal = True
            db.session.commit()  # 提交更改

            # 返回用户信息
            user_info = {
                'name': user.name,
                'phone': user.phone,
                'wx_openid': user.wx_openid,
                'principal': user.principal  # 返回更新后的principal值
            }
            return jsonify(user_info), 200  # 匹配成功，返回用户信息
        else:
            # 如果姓名或密码不匹配，返回失败信息
            return jsonify({'message': '姓名或密码错误'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#15项清单的查询权限人员（返回所有query_15为True的姓名和号码）
@blue.route('/user/query_15', methods=['GET'])
def get_users_query_15():
    # 查询所有query_15为True的用户
    users = UserModel.query.filter_by(query_15=True).all()

    # 格式化返回的结果
    result = []
    for user in users:
        result.append({
            'name': user.name,
            'phone': user.phone
        })

    return jsonify(result), 200  # 返回查询结果

#15项清单查询权限人员的添加（返回所有query_15为True的姓名和号码）
@blue.route('/user/add', methods=['POST'])
def add_user_query_15():
    # 获取请求中的数据
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户已存在且query_15为True，返回"已存在"
        if user.query_15:
            return jsonify({"message": "已存在"}), 400  # 已存在并且query_15为True
        else:
            # 如果用户存在且query_15为False，更新query_15为True
            user.query_15 = True
            db.session.commit()  # 提交更改
            # 返回所有query_15为True的用户信息
            users = UserModel.query.filter_by(query_15=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 更新成功，返回所有query_15为True的用户信息
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#15项清单查询权限人员的删除（返回所有query_15为True的姓名和号码）
@blue.route('/user/delete', methods=['POST'])
def delete_user_query_15():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户存在，检查query_15是否为True
        if user.query_15:
            # 如果query_15为True，删除该用户
            db.session.delete(user)
            db.session.commit()  # 提交删除操作
            # 返回所有query_15为True的用户信息
            users = UserModel.query.filter_by(query_15=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 删除成功，返回所有query_15为True的用户信息
        else:
            # 如果query_15为False，无法删除
            return jsonify({'message': '该用户无法删除，query_15为False'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#15项清单修改权限人员（返回所有alter_15为true的姓名和号码）
@blue.route('/user/alter_15', methods=['GET'])
def get_users_alter_15():
    # 查询所有alter_15为True的用户
    users = UserModel.query.filter_by(alter_15=True).all()

    # 格式化返回的结果
    result = []
    for user in users:
        result.append({
            'name': user.name,
            'phone': user.phone
        })

    return jsonify(result), 200  # 返回查询结果

#15项清单修改权限人员的添加（返回所有alter_15为true的姓名和号码）
@blue.route('/user/add', methods=['POST'])
def add_user_alter_15():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户已存在且alter_15为True，返回"已存在"
        if user.alter_15:
            return jsonify({"message": "已存在"}), 400  # 已存在并且alter_15为True
        else:
            # 如果用户存在且alter_15为False，更新alter_15为True
            user.alter_15 = True
            db.session.commit()  # 提交更改
            # 返回所有alter_15为True的用户信息
            users = UserModel.query.filter_by(alter_15=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 更新成功，返回所有alter_15为True的用户信息
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#15项清单修改权限人员的删除（返回所有alter_15为true的姓名和号码）
@blue.route('/user/delete', methods=['POST'])
def delete_user_alter_15():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户存在，检查alter_15是否为True
        if user.alter_15:
            # 如果alter_15为True，删除该用户
            db.session.delete(user)
            db.session.commit()  # 提交删除操作
            # 返回所有alter_15为True的用户信息
            users = UserModel.query.filter_by(alter_15=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 删除成功，返回所有alter_15为True的用户信息
        else:
            # 如果alter_15为False，无法删除
            return jsonify({'message': '该用户无法删除，alter_15为False'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#政策文件修改权限人员（返回所有alter_zc为true的姓名和电话）
@blue.route('/user/alter_zc', methods=['GET'])
def get_users_alter_zc():
    # 查询所有alter_zc为True的用户
    users = UserModel.query.filter_by(alter_zc=True).all()

    # 格式化返回的结果
    result = []
    for user in users:
        result.append({
            'name': user.name,
            'phone': user.phone
        })

    return jsonify(result), 200  # 返回查询结果

#政策文件修改权限人员的添加（返回所有alter_zc为true的姓名和电话）
@blue.route('/user/add', methods=['POST'])
def add_user_alter_zc():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户已存在且alter_zc为True，返回"已存在"
        if user.alter_zc:
            return jsonify({"message": "已存在"}), 400  # 已存在并且alter_zc为True
        else:
            # 如果用户存在且alter_zc为False，更新alter_zc为True
            user.alter_zc = True
            db.session.commit()  # 提交更改
            # 返回所有alter_zc为True的用户信息
            users = UserModel.query.filter_by(alter_zc=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 更新成功，返回所有alter_zc为True的用户信息
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#政策文件修改权限人员的删除（返回所有alter_zc为true的姓名和电话）
@blue.route('/user/delete', methods=['POST'])
def delete_user_alter_zc():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户存在，检查alter_zc是否为True
        if user.alter_zc:
            # 如果alter_zc为True，删除该用户
            db.session.delete(user)
            db.session.commit()  # 提交删除操作
            # 返回所有alter_zc为True的用户信息
            users = UserModel.query.filter_by(alter_zc=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 删除成功，返回所有alter_zc为True的用户信息
        else:
            # 如果alter_zc为False，无法删除
            return jsonify({'message': '该用户无法删除，alter_zc为False'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#典型案例修改权限人员（返回所有alter_model为true的姓名和电话）
@blue.route('/user/alter_model', methods=['GET'])
def get_users_alter_model():
    # 查询所有alter_model为True的用户
    users = UserModel.query.filter_by(alter_model=True).all()

    # 格式化返回的结果
    result = []
    for user in users:
        result.append({
            'name': user.name,
            'phone': user.phone
        })

    return jsonify(result), 200  # 返回查询结果


#典型案例修改权限人员的添加（返回所有alter_model为true的姓名和电话）
@blue.route('/user/add', methods=['POST'])
def add_user_alter_model():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户已存在且alter_model为True，返回"已存在"
        if user.alter_model:
            return jsonify({"message": "已存在"}), 400  # 已存在并且alter_model为True
        else:
            # 如果用户存在且alter_model为False，更新alter_model为True
            user.alter_model = True
            db.session.commit()  # 提交更改
            # 返回所有alter_model为True的用户信息
            users = UserModel.query.filter_by(alter_model=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 更新成功，返回所有alter_model为True的用户信息
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#典型案例修改权限人员的删除（返回所有alter_model为true的姓名和电话）
@blue.route('/user/delete', methods=['POST'])
def delete_user_alter_model():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户存在，检查alter_model是否为True
        if user.alter_model:
            # 如果alter_model为True，删除该用户
            db.session.delete(user)
            db.session.commit()  # 提交删除操作
            # 返回所有alter_model为True的用户信息
            users = UserModel.query.filter_by(alter_model=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 删除成功，返回所有alter_model为True的用户信息
        else:
            # 如果alter_model为False，无法删除
            return jsonify({'message': '该用户无法删除，alter_model为False'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

# 查询alter_progress为True的用户姓名和手机号
@blue.route('/user/alter_progress', methods=['GET'])
def get_users_alter_progress():
    # 查询所有alter_progress为True的用户
    users = UserModel.query.filter_by(alter_progress=True).all()

    # 格式化返回的结果
    result = []
    for user in users:
        result.append({
            'name': user.name,
            'phone': user.phone
        })

    return jsonify(result), 200  # 返回查询结果

# 添加记录接口（验证用户信息、检查alter_progress并更新）
@blue.route('/user/add', methods=['POST'])
def add_user_alter_progress():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户已存在且alter_progress为True，返回"已存在"
        if user.alter_progress:
            return jsonify({"message": "已存在"}), 400  # 已存在并且alter_progress为True
        else:
            # 如果用户存在且alter_progress为False，更新alter_progress为True
            user.alter_progress = True
            db.session.commit()  # 提交更改
            # 返回所有alter_progress为True的用户信息
            users = UserModel.query.filter_by(alter_progress=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 更新成功，返回所有alter_progress为True的用户信息
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404


# 删除记录接口（验证用户信息、检查alter_progress并删除）
@blue.route('/user/delete', methods=['POST'])
def delete_user_alter_progress():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户存在，检查alter_progress是否为True
        if user.alter_progress:
            # 如果alter_progress为True，删除该用户
            db.session.delete(user)
            db.session.commit()  # 提交删除操作
            # 返回所有alter_progress为True的用户信息
            users = UserModel.query.filter_by(alter_progress=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 删除成功，返回所有alter_progress为True的用户信息
        else:
            # 如果alter_progress为False，无法删除
            return jsonify({'message': '该用户无法删除，alter_progress为False'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404


# ==================== 15projects 表接口 ====================

# 1. 查询所有project_name
@blue.route('/api/15projects/names', methods=['GET'])
def get_all_project_names():
    """
    查询所有15projects表的project_name字段
    """
    try:
        from app.models import Projects15
        projects = Projects15.query.with_entities(Projects15.project_name).all()
        names = [p.project_name for p in projects]
        return jsonify({'success': True, 'data': names}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'查询失败: {str(e)}'}), 500

# 2. 根据project_name查objectives
@blue.route('/api/15projects/objectives', methods=['GET'])
def get_objectives_by_project_name():
    """
    根据project_name查询objectives字段
    前端传递参数project_name
    """
    try:
        from app.models import Projects15
        project_name = request.args.get('project_name')
        if not project_name:
            return jsonify({'success': False, 'message': '缺少project_name参数'}), 400
        project = Projects15.query.filter_by(project_name=project_name).first()
        if not project:
            return jsonify({'success': False, 'message': '未找到该项目'}), 404
        return jsonify({'success': True, 'data': {'objectives': project.objectives}}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'查询失败: {str(e)}'}), 500

# 3. 增加记录
@blue.route('/api/15projects', methods=['POST'])
def add_15project():
    """
    新增一条15projects表记录
    """
    try:
        from app.models import Projects15, db
        data = request.json
        # 只校验部分必填字段，具体可根据实际表结构调整
        required_fields = ['serial_number', 'city', 'county', 'universities', 'project_name', 'implementing_institutions', 'is_key_project', 'project_type', 'start_date', 'end_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'缺少必要参数: {field}'}), 400
        new_project = Projects15(
            serial_number=data.get('serial_number'),
            city=data.get('city'),
            county=data.get('county'),
            universities=data.get('universities'),
            project_name=data.get('project_name'),
            implementing_institutions=data.get('implementing_institutions'),
            is_key_project=data.get('is_key_project'),
            involved_areas=data.get('involved_areas'),
            project_type=data.get('project_type'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            background=data.get('background'),
            content_and_measures=data.get('content_and_measures'),
            objectives=data.get('objectives'),
            contacts=data.get('contacts'),
            remarks=data.get('remarks')
        )
        db.session.add(new_project)
        db.session.commit()
        return jsonify({'success': True, 'message': '添加成功', 'id': new_project.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'添加失败: {str(e)}'}), 500

# 4. 修改记录
@blue.route('/api/15projects/<int:project_id>', methods=['PUT'])
def update_15project(project_id):
    """
    修改指定15projects表记录
    前端传递要修改的字段及新值
    """
    try:
        from app.models import Projects15, db
        data = request.json
        project = Projects15.query.get(project_id)
        if not project:
            return jsonify({'success': False, 'message': '未找到该项目'}), 404
        # 只更新前端传递的字段
        for key, value in data.items():
            if hasattr(project, key):
                setattr(project, key, value)
        db.session.commit()
        return jsonify({'success': True, 'message': '修改成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'修改失败: {str(e)}'}), 500