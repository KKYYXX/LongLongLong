#放视图
import os
from flask import Blueprint,request,jsonify,render_template
from werkzeug.utils import secure_filename
from app.models import ZCDocument
from app.plugins import db
from sqlalchemy import func
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import UserModel, ZCDocument,newsModel

from flask import request, jsonify, send_from_directory


blue = Blueprint('blue',__name__)

#视图

# ==================== ZCDocument 表接口 ====================

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
            '''documents_list.append({
                #'user_id': doc.user_id,
                'file_url': doc.file_url,
                'file_type': doc.file_type,
                'original_name': doc.original_name,
                'file_size': doc.file_size,
                'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M:%S') if doc.uploaded_at else None
            })'''
            # views.py 中 get_all_zcdocuments 函数中：
            documents_list.append({
                'file_name': doc.original_name,  # 改名为更通俗
                'file_size': doc.file_size,
                'file_url': doc.file_url,
                'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M:%S') if doc.uploaded_at else None,
                'id': doc.id

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
    - file_url: 文件访问URL
    - file_type: 文件类型(pdf/doc/docx)（兼容filetype参数）
    - original_name: 原始文件名
    - file_size: 文件大小(字节)
    """
    try:
        # 统一获取请求数据（支持JSON和表单格式）
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()  # 转换为字典便于处理

        # 提取参数（兼容常见拼写错误，如filetype -> file_type）
        file_url = data.get('file_url', '').strip()
        # 优先取file_type，若不存在则尝试取filetype（兼容前端拼写错误）
        file_type = data.get('file_type', data.get('filetype', '')).strip().lower()
        original_name = data.get('original_name', '').strip()
        file_size_str = str(data.get('file_size', '')).strip()

        # 参数验证：检查必填参数是否存在
        required_params = [
            ('file_url', file_url),
            ('file_type', file_type),
            ('original_name', original_name),
            ('file_size', file_size_str)
        ]
        for param_name, param_value in required_params:
            if not param_value:
                return jsonify({
                    'success': False,
                    'message': f'缺少必要参数：{param_name}'
                }), 400

        # 验证文件类型
        allowed_types = ['pdf', 'doc', 'docx']
        if file_type not in allowed_types:
            return jsonify({
                'success': False,
                'message': f'文件类型必须是：{", ".join(allowed_types)}'
            }), 400




        # 验证file_url格式（基础校验）
        if not (file_url.startswith(('http://', 'https://')) or os.path.isfile(file_url)):
            return jsonify({
                'success': False,
                'message': 'file_url必须是有效的HTTP/HTTPS链接或本地文件路径'
            }), 400

        # 创建并保存记录
        new_document = ZCDocument(
            file_url=file_url,
            file_type=file_type,
            original_name=original_name,
            file_size=file_size_str,
            uploaded_at=datetime.utcnow()
        )
        db.session.add(new_document)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '添加成功',
            'data': {
                'id': new_document.id,
                'file_name': new_document.original_name,
                'file_size': str(new_document.file_size),  # 强制转为字符串
                'file_url': new_document.file_url,
                'file_type': new_document.file_type,
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
                'file_name': m.file_name,
                'file_type': m.file_type,
                'file_size': m.file_size,
                'file_url': m.file_url,
                'model_name':m.model_name,
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
        #user_id = data.get('user_id')
        file_name = data.get('file_name')
        file_type = data.get('file_type')
        file_size = data.get('file_size')
        file_url = data.get('file_url')
        model_name = data.get('model_name')
        #has_text = data.get('has_text', True)
        #has_images = data.get('has_images', False)
        #video_url = data.get('video_url')
        # 校验必填
        if not all([file_name, file_type, file_size, file_url]):
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
            #user_id=user_id,
            file_name=file_name,
            file_type=file_type,
            file_size=file_size,
            file_url=file_url,
            model_name=model_name,
            #has_text=bool(has_text),
            #has_images=bool(has_images),
            #video_url=video_url,
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
#用户注册接口
@blue.route('/user/register', methods=['POST'])
def register_user():
    data = request.json

    name = data.get('name')
    phone = data.get('phone')
    wx_openid = data.get('wx_openid')
    password = data.get('password')

    if not all([name, phone, wx_openid, password]):
        return jsonify({'success': False, 'message': '请填写所有字段'}), 400

    # 检查手机号是否已存在
    if UserModel.query.filter_by(phone=phone).first():
        return jsonify({'success': False, 'message': '该手机号已注册'}), 409

    # 创建用户实例（密码为明文）
    new_user = UserModel(
        name=name,
        phone=phone,
        wx_openid=wx_openid,
        password=password,
        principal=False  # 默认无权限
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': '注册成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'注册失败: {str(e)}'}), 500


#普通登录接口
@blue.route('/user/common_login', methods=['POST'])
def user_common_login():
    data = request.json
    phone = data.get('phone')
    wx_openid = data.get('wx_openid')
    password = data.get('password')

    if not password:
        return jsonify({'success': False, 'message': '请输入密码'}), 400

    user = None

    if phone:
        user = UserModel.query.filter_by(phone=phone).first()
    elif wx_openid:
        user = UserModel.query.filter_by(wx_openid=wx_openid).first()
    else:
        return jsonify({'success': False, 'message': '请提供手机号或微信号'}), 400

    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    if user.password != password:
        return jsonify({'success': False, 'message': '密码错误'}), 401

    return jsonify({
        'success': True,
        'message': '登录成功',
        'user': {
            'name': user.name,
            'phone': user.phone,
            'wx_openid': user.wx_openid,
            'principal': user.principal,
            'alter_15': user.alter_15,
            'query_15': user.query_15,
            'alter_zc': user.alter_zc,
            'alter_model': user.alter_model,
            'alter_progress': user.alter_progress
        }
    })


#权限管理登录接口
@blue.route('/user/principal_login', methods=['POST'])
def user_principal_login():
    data = request.json
    phone = data.get('phone')
    wx_openid = data.get('wx_openid')
    password = data.get('password')

    if not password:
        return jsonify({'success': False, 'message': '请输入密码'}), 400

    user = None

    if phone:
        user = UserModel.query.filter_by(phone=phone).first()
    elif wx_openid:
        user = UserModel.query.filter_by(wx_openid=wx_openid).first()
    else:
        return jsonify({'success': False, 'message': '请提供手机号或微信号'}), 400

    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    if user.password != password:
        return jsonify({'success': False, 'message': '密码错误'}), 401

    if not user.principal:
        return jsonify({'success': False, 'message': '该用户无权限'}), 403

    return jsonify({
        'success': True,
        'message': '登录成功',
        'user': {
            'name': user.name,
            'phone': user.phone,
            'wx_openid': user.wx_openid,
            'principal': user.principal
        }
    })



#转让页面接口（返回姓名、号码、密码）
@blue.route('/user/transfer_principal', methods=['POST'])
def transfer_principal():
    # 被转让人信息（接收人）
    name = request.form.get('name')
    phone = request.form.get('phone')
    wx_openid = request.form.get('wx_openid')

    # 当前负责人手机号（发起人）
    current_phone = request.form.get('current_phone')

    if not all([name, phone, wx_openid, current_phone]):
        return jsonify({'message': '请提供完整信息'}), 400

    # 查询被转让人
    target_user = UserModel.query.filter_by(phone=phone).first()
    if not target_user:
        return jsonify({'message': '被转让用户不存在'}), 404

    # 校验目标用户信息是否匹配
    if target_user.name != name or target_user.wx_openid != wx_openid:
        return jsonify({'message': '被转让用户信息有误，请确认'}), 400

    # 校验目标用户不能已是负责人
    if target_user.principal:
        return jsonify({'message': '该用户已是负责人，不能转让'}), 403

    # 查询当前负责人
    current_user = UserModel.query.filter_by(phone=current_phone).first()
    if not current_user or not current_user.principal:
        return jsonify({'message': '当前用户无权进行转让'}), 403

    try:
        # 执行转让操作
        current_user.principal = False
        target_user.principal = True

        db.session.commit()
        return jsonify({'message': '负责人转让成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'转让失败: {str(e)}'}), 500


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
@blue.route('/user/query_15_add', methods=['POST'])
def add_user_query_15():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    if not all([name, phone]):
        return jsonify({'message': '缺少必要参数'}), 400

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户已存在且 query_15 为 True，返回"已存在"
        if user.query_15:
            return jsonify({"message": "已存在"}), 400
        else:
            # 如果用户存在且 query_15 为 False，更新 query_15 为 True
            user.query_15 = True
            db.session.commit()
            # 返回所有 query_15 为 True 的用户信息
            users = UserModel.query.filter_by(query_15=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404



#15项清单查询权限人员的删除（返回所有query_15为True的姓名和号码）
@blue.route('/user/query_15_delete', methods=['POST'])
def delete_user_query_15():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户存在，检查 query_15 是否为 True
        if user.query_15:
            # 如果 query_15 为 True，更新为 False
            user.query_15 = False
            db.session.commit()  # 提交更改
            # 返回所有 query_15 为 True 的用户信息
            users = UserModel.query.filter_by(query_15=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 删除成功，返回所有 query_15 为 True 的用户信息
        else:
            # 如果 query_15 为 False，无法删除
            return jsonify({'message': '该用户无法删除，本就没有该权限'}), 400
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

#15项清单修改权限人员的添加（返回所有alter_15为True的姓名和号码）
@blue.route('/user/alter_15_add', methods=['POST'])
def add_user_alter_15():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    if not all([name, phone]):
        return jsonify({'message': '缺少必要参数'}), 400

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户已存在且 alter_15 为 True，返回"已存在"
        if user.alter_15:
            return jsonify({"message": "已存在"}), 400
        else:
            # 如果用户存在且 alter_15 为 False，更新 alter_15 为 True
            user.alter_15 = True
            db.session.commit()
            # 返回所有 alter_15 为 True 的用户信息
            users = UserModel.query.filter_by(alter_15=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#15项清单修改权限人员的删除（返回所有alter_15为True的姓名和号码）
@blue.route('/user/alter_15_delete', methods=['POST'])
def delete_user_alter_15():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户存在，检查 query_15 是否为 True
        if user.alter_15:
            # 如果 alter_15 为 True，更新为 False
            user.alter_15 = False
            db.session.commit()  # 提交更改
            # 返回所有 alter_15 为 True 的用户信息
            users = UserModel.query.filter_by(alter_15=True).all()
            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })
            return jsonify(result), 200  # 删除成功，返回所有 query_15 为 True 的用户信息
        else:
            # 如果 query_15 为 False，无法删除
            return jsonify({'message': '该用户无法删除，本就没有该权限'}), 400
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
@blue.route('/user/alter_zc_add', methods=['POST'])
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
@blue.route('/user/alter_zc_delete', methods=['POST'])
def delete_user_alter_zc():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户存在，检查alter_zc是否为True
        if user.alter_zc:
            # 如果alter_zc为True，更新alter_zc为False
            user.alter_zc = False
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
            return jsonify({'message': '该用户无法删除，本就没有该权限'}), 400
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
@blue.route('/user/alter_model_add', methods=['POST'])
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
@blue.route('/user/alter_model_delete', methods=['POST'])
def delete_user_alter_model():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户存在，检查alter_model是否为True
        if user.alter_model:
            # 如果alter_model为True，更新alter_model为False
            user.alter_model = False
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
            return jsonify({'message': '该用户无法删除，本就没有该权限'}), 400
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
@blue.route('/user/alter_progress_add', methods=['POST'])
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
@blue.route('/user/alter_progress_delete', methods=['POST'])
def delete_user_alter_progress():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')
    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()
    if user:
        # 如果用户存在，检查alter_progress是否为True
        if user.alter_progress:
            # 如果alter_progress为True，更新alter_progress为False
            user.alter_progress = False
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
            return jsonify({'message': '该用户无法删除，本就没有该权限'}), 400
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


# 2. 根据id查询Projects15的16项信息
"""
    根据id查询Projects15表的所有16项信息
    前端传递参数id
    """

# 2. 根据id查询Projects15的16项信息
"""
    根据id查询Projects15表的所有16项信息
    路径参数：project_id - 项目ID
    """
@blue.route('/api/15projects/detail/<int:project_id>', methods=['GET'])
def get_project_detail_by_id(project_id):
    """
    根据id查询Projects15表的所有16项信息
    路径参数：project_id - 项目ID
    """
    try:
        from app.models import Projects15
        # 直接使用路径参数中的project_id查询
        project = Projects15.query.get(project_id)
        if not project:
            return jsonify({'success': False, 'message': f'未找到id为{project_id}的项目'}), 404

        # 返回所有16项信息
        return jsonify({
            'success': True,
            'data': {
                'id': project.id,
                'serial_number': float(project.serial_number) if project.serial_number else None,
                'city': project.city,
                'county': project.county,
                'universities': project.universities,
                'project_name': project.project_name,
                'implementing_institutions': project.implementing_institutions,
                'is_key_project': project.is_key_project,
                'involved_areas': project.involved_areas,
                'project_type': project.project_type,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'background': project.background,
                'content_and_measures': project.content_and_measures,
                'objectives': project.objectives,
                'contacts': project.contacts,
                'remarks': project.remarks
            }
        }), 200
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
        field_name = data.get('field_name')  # 要修改的字段名
        new_value = data.get('new_value')  # 新值

        if not field_name:
            return jsonify({'success': False, 'message': '缺少字段名'}), 400

        if new_value is None:
            return jsonify({'success': False, 'message': '缺少新值'}), 400

        # 查找项目
        project = Projects15.query.get(project_id)
        if not project:
            return jsonify({'success': False, 'message': '未找到该项目'}), 404

        # 字段映射：前端字段名 -> 数据库列名
        field_mapping = {
            'serialNumber': 'serial_number',
            'cityLevel': 'city',
            'pairedCounty': 'county',
            'pairedInstitution': 'universities',
            'projectName': 'project_name',
            'implementationUnit': 'implementing_institutions',
            'isKeyProject': 'is_key_project',
            'involvedAreas': 'involved_areas',
            'projectType': 'project_type',
            'startDate': 'start_date',
            'endDate': 'end_date',
            'background': 'background',
            'content': 'content_and_measures',
            'objectives': 'objectives',
            'contacts': 'contacts',
            'remarks': 'remarks'
        }

        # 获取数据库字段名
        db_field_name = field_mapping.get(field_name, field_name)

        # 检查字段是否存在
        if not hasattr(project, db_field_name):
            return jsonify({
                'success': False,
                'message': f'字段 {field_name} 不存在或无法修改'
            }), 400

        # 获取旧值
        old_value = getattr(project, db_field_name)

        # 更新字段值
        setattr(project, db_field_name, new_value)

        # 提交到数据库
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '修改成功',
            'data': {
                'field_name': field_name,
                'old_value': old_value,
                'new_value': new_value
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"修改项目失败: {str(e)}")  # 添加日志
        return jsonify({
            'success': False,
            'message': f'修改失败: {str(e)}'
        }), 500


# 5. 删除记录
@blue.route('/api/15projects/<int:project_id>', methods=['DELETE'])
def delete_15project(project_id):
    """
    删除指定的15projects表记录
    参数：project_id - 要删除的记录ID
    """
    try:
        from app.models import Projects15, db
        project = Projects15.query.get(project_id)
        if not project:
            return jsonify({'success': False, 'message': f'记录ID {project_id} 不存在'}), 404

        db.session.delete(project)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功', 'deleted_id': project_id}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'}), 500


# 6. 通过项目名称查找项目ID
@blue.route('/api/15projects/search', methods=['GET'])
def search_project_by_name():
    """
    根据项目名称查找项目ID
    参数：project_name - 项目名称
    返回：项目ID和基本信息
    """
    try:
        from app.models import Projects15

        project_name = request.args.get('project_name')
        if not project_name:
            return jsonify({
                'success': False,
                'message': '缺少必要参数：project_name'
            }), 400

        # 在数据库中查找项目
        project = Projects15.query.filter_by(project_name=project_name).first()

        if not project:
            return jsonify({
                'success': False,
                'message': f'未找到项目名称：{project_name}'
            }), 404

        # 返回项目信息（包含ID）
        return jsonify({
            'success': True,
            'message': '查询成功',
            'data': {
                'id': project.id,
                'project_name': project.project_name,
                'project_type': project.project_type,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'background': project.background,
                'objectives': project.objectives,
                'remarks': project.remarks
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'查询失败: {str(e)}'
        }), 500

# ==================== progress表接口 ====================

# 1. 查询接口：根据project_name查询所有记录的practice_time字段
@blue.route('/api/progress/times', methods=['GET'])
def get_progress_times():
    """
    根据project_name查询所有记录的practice_time字段
    参数：project_name - 项目名称
    """
    try:
        from app.models import ProgressModel
        project_name = request.args.get('project_name')
        
        if not project_name:
            return jsonify({
                'success': False, 
                'message': '缺少必要参数：project_name'
            }), 400

        # 查询指定项目的所有记录
        progress_records = ProgressModel.query.filter_by(project_name=project_name).all()
        
        # 提取practice_time字段
        times = []
        for record in progress_records:
            times.append({
                'practice_time': record.practice_time.strftime('%Y-%m-%d %H:%M:%S') if record.practice_time else None
            })

        return jsonify({
            'success': True,
            'message': '查询成功',
            'data': times,
            'total_count': len(times)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'查询失败: {str(e)}'
        }), 500


# 2. 查询接口：根据project_name和practice_time查询记录的详细信息
@blue.route('/api/progress/detail', methods=['GET'])
def get_progress_detail():
    """
    根据project_name和practice_time查询记录的详细信息
    参数：project_name - 项目名称
    参数：practice_time - 实践时间（格式：YYYY-MM-DD HH:MM:SS）
    """
    try:
        from app.models import ProgressModel
        from datetime import datetime
        
        project_name = request.args.get('project_name')
        practice_time_str = request.args.get('practice_time')
        
        if not project_name or not practice_time_str:
            return jsonify({
                'success': False, 
                'message': '缺少必要参数：project_name 或 practice_time'
            }), 400

        # 将时间字符串转换为datetime对象
        try:
            practice_time = datetime.strptime(practice_time_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'message': '时间格式错误，请使用 YYYY-MM-DD 格式'
            }), 400

        # 查询指定记录
        record = ProgressModel.query.filter_by(
            project_name=project_name,
            practice_time=practice_time
        ).first()

        if not record:
            return jsonify({
                'success': False,
                'message': '未找到对应的记录'
            }), 404

        # 返回详细信息
        detail = {
            'project_name': record.project_name,
            'practice_time': record.practice_time.strftime('%Y-%m-%d ') if record.practice_time else None,
            'practice_location': record.practice_location,
            'practice_members': record.practice_members,
            'practice_image_url': record.practice_image_url,
            'practice_video_url': record.practice_video_url,
            'news': record.news
        }

        return jsonify({
            'success': True,
            'message': '查询成功',
            'data': detail
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'查询失败: {str(e)}'
        }), 500


# 3. 删除接口：根据project_name和practice_time删除记录
@blue.route('/api/progress/delete', methods=['DELETE'])
def delete_progress_record():
    """
    根据project_name和practice_time删除记录
    参数：project_name - 项目名称
    参数：practice_time - 实践时间（格式：YYYY-MM-DD HH:MM:SS）
    """
    try:
        from app.models import ProgressModel
        from datetime import datetime
        
        data = request.get_json() if request.is_json else request.form
        
        project_name = data.get('project_name')
        practice_time_str = data.get('practice_time')
        
        if not project_name or not practice_time_str:
            return jsonify({
                'success': False, 
                'message': '缺少必要参数：project_name 或 practice_time'
            }), 400

        # 将时间字符串转换为datetime对象
        try:
            practice_time = datetime.strptime(practice_time_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'message': '时间格式错误，请使用 YYYY-MM-DD 格式'
            }), 400

        # 查找要删除的记录
        record = ProgressModel.query.filter_by(
            project_name=project_name,
            practice_time=practice_time
        ).first()

        if not record:
            return jsonify({
                'success': False,
                'message': '未找到对应的记录'
            }), 404

        # 保存删除前的信息用于返回
        deleted_info = {
            'project_name': record.project_name,
            'practice_time': record.practice_time.strftime('%Y-%m-%d ') if record.practice_time else None
        }

        # 删除记录
        db.session.delete(record)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '删除成功',
            'deleted_record': deleted_info
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }), 500


# 4. 修改接口：根据project_name和practice_time修改记录
@blue.route('/api/progress/update', methods=['PUT'])
def update_progress_record():
    """
    根据project_name和practice_time修改记录
    参数：project_name - 项目名称
    参数：practice_time - 实践时间（格式：YYYY-MM-DD HH:MM:SS）
    可选参数：practice_location, practice_members, practice_image_url, news
    """
    try:
        from app.models import ProgressModel
        from datetime import datetime
        
        data = request.get_json()
        
        project_name = data.get('project_name')
        practice_time_str = data.get('practice_time')
        
        if not project_name or not practice_time_str:
            return jsonify({
                'success': False, 
                'message': '缺少必要参数：project_name 或 practice_time'
            }), 400

        # 将时间字符串转换为datetime对象
        try:
            practice_time = datetime.strptime(practice_time_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'message': '时间格式错误，请使用 YYYY-MM-DD 格式'
            }), 400

        # 查找要修改的记录
        record = ProgressModel.query.filter_by(
            project_name=project_name,
            practice_time=practice_time
        ).first()

        if not record:
            return jsonify({
                'success': False,
                'message': '未找到对应的记录'
            }), 404

        # 更新字段（只更新提供的字段）
        if 'practice_location' in data:
            record.practice_location = data['practice_location']
        if 'practice_members' in data:
            record.practice_members = data['practice_members']
        if 'practice_image_url' in data:
            record.practice_image_url = data['practice_image_url']
        if 'practice_video_url' in data:
            record.practice_image_url = data['practice_video_url']
        if 'news' in data:
            record.news = data['news']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': '修改成功',
            'data': {
                'project_name': record.project_name,
                'practice_time': record.practice_time.strftime('%Y-%m-%d') if record.practice_time else None,
                'practice_location': record.practice_location,
                'practice_members': record.practice_members,
                'practice_image_url': record.practice_image_url,
                'news': record.news,
                'practice_video_url': record.practice_video_url
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'修改失败: {str(e)}'
        }), 500


# 5. 添加接口：添加新的progress记录
@blue.route('/api/progress/add', methods=['POST'])
def add_progress_record():
    """
    添加新的progress记录
    参数：project_name, practice_time, practice_location, practice_members, news
    可选参数：practice_image_url
    """
    try:
        from app.models import ProgressModel, Projects15
        from datetime import datetime
        
        data = request.get_json() if request.is_json else request.form
        
        # 获取必要参数
        project_name = data.get('project_name')
        practice_time_str = data.get('practice_time')
        practice_location = data.get('practice_location')
        practice_members = data.get('practice_members')
        news = data.get('news')
        practice_image_url = data.get('practice_image_url')
        practice_video_url = data.get('practice_video_url')

        # 参数验证
        if not all([project_name, practice_time_str, practice_location, practice_members, news]):
            return jsonify({
                'success': False,
                'message': '缺少必要参数：project_name, practice_time, practice_location, practice_members, news'
            }), 400

        # 验证project_name是否存在于15projects表中
        project = Projects15.query.filter_by(project_name=project_name).first()
        if not project:
            return jsonify({
                'success': False,
                'message': f'项目名称 "{project_name}" 在15projects表中不存在'
            }), 400

        # 将时间字符串转换为datetime对象
        try:
            practice_time = datetime.strptime(practice_time_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'message': '时间格式错误，请使用 YYYY-MM-DD 格式'
            }), 400

        # 检查是否已存在相同的记录
        existing_record = ProgressModel.query.filter_by(
            project_name=project_name,
            practice_time=practice_time
        ).first()

        if existing_record:
            return jsonify({
                'success': False,
                'message': '该项目的该时间点已存在记录'
            }), 400

        # 创建新记录
        new_record = ProgressModel(
            project_name=project_name,
            practice_time=practice_time,
            practice_location=practice_location,
            practice_members=practice_members,
            practice_image_url=practice_image_url,
            news=news,
            practice_video_url = practice_video_url
        )

        # 添加到数据库
        db.session.add(new_record)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '添加成功',
            'data': {
                'project_name': new_record.project_name,
                'practice_time': new_record.practice_time.strftime('%Y-%m-%d') if new_record.practice_time else None,
                'practice_location': new_record.practice_location,
                'practice_members': new_record.practice_members,
                'practice_image_url': new_record.practice_image_url,
                'news': new_record.news,
                'practice_video_url': new_record.practice_video_url

            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'添加失败: {str(e)}'
        }), 500


# ==================== newsModel 表接口 ====================

# 1. 查询接口：根据model_name查询记录
@blue.route('/api/news', methods=['GET'])
def query_news_by_model_name():
    """
    根据model_name查询newsModel表中的相关记录
    参数：model_name - 案例名称
    """
    try:
        from app.models import newsModel
        
        model_name = request.args.get('model_name')
        
        if not model_name:
            return jsonify({
                'success': False,
                'message': '缺少必要参数：model_name'
            }), 400

        # 查询指定model_name的所有记录
        news_records = newsModel.query.filter_by(model_name=model_name).all()
        
        # 格式化返回结果
        result = []
        for record in news_records:
            result.append({
                'id': record.id,
                'model_name': record.model_name,
                'news_url': record.news_url,
                'news_title': record.news_title
            })

        return jsonify({
            'success': True,
            'message': '查询成功',
            'data': result,
            'total_count': len(result)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'查询失败: {str(e)}'
        }), 500


# 2. 删除接口：根据model_name删除记录
@blue.route('/api/news', methods=['DELETE'])
def delete_news_by_model_name():
    """
    根据model_name删除newsModel表中的所有相关记录
    参数：model_name - 案例名称
    """
    try:
        from app.models import newsModel
        
        data = request.get_json() if request.is_json else request.form
        
        model_name = data.get('model_name')
        
        if not model_name:
            return jsonify({
                'success': False,
                'message': '缺少必要参数：model_name'
            }), 400

        # 查找要删除的记录
        news_records = newsModel.query.filter_by(model_name=model_name).all()
        
        if not news_records:
            return jsonify({
                'success': False,
                'message': f'未找到model_name为"{model_name}"的记录'
            }), 404

        # 保存删除前的信息用于返回
        deleted_count = len(news_records)
        deleted_info = []
        for record in news_records:
            deleted_info.append({
                'id': record.id,
                'model_name': record.model_name,
                'news_url': record.news_url,
                'news_title': record.news_title
            })

        # 删除所有匹配的记录
        for record in news_records:
            db.session.delete(record)
        
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'删除成功，共删除{deleted_count}条记录',
            'deleted_records': deleted_info,
            'deleted_count': deleted_count
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }), 500


# 3. 添加接口：添加新的newsModel记录
@blue.route('/api/news', methods=['POST'])
def add_news_record():
    """
    添加新的newsModel记录
    参数：model_name, news_url, news_title
    """
    try:
        from app.models import newsModel
        
        data = request.get_json() if request.is_json else request.form
        
        # 获取参数
        model_name = data.get('model_name')
        news_url = data.get('news_url')
        news_title = data.get('news_title')

        # 参数验证
        if not all([model_name, news_url, news_title]):
            return jsonify({
                'success': False,
                'message': '缺少必要参数：model_name, news_url, news_title'
            }), 400

        # 创建新记录
        new_record = newsModel(
            model_name=model_name,
            news_url=news_url,
            news_title=news_title
        )

        # 添加到数据库
        db.session.add(new_record)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '添加成功',
            'data': {
                'id': new_record.id,
                'model_name': new_record.model_name,
                'news_url': new_record.news_url,
                'news_title': new_record.news_title
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'添加失败: {str(e)}'
        }), 500


# ==================== videoModel 表接口 ====================

# 1. 查询接口：根据model_name查询记录
@blue.route('/api/video', methods=['GET'])
def query_video_by_model_name():
    """
    根据model_name查询videoModel表中的相关记录
    参数：model_name - 案例名称
    """
    try:
        from app.models import videoModel
        
        model_name = request.args.get('model_name')
        
        if not model_name:
            return jsonify({
                'success': False,
                'message': '缺少必要参数：model_name'
            }), 400

        # 查询指定model_name的所有记录
        video_records = videoModel.query.filter_by(model_name=model_name).all()
        
        # 格式化返回结果
        result = []
        for record in video_records:
            result.append({
                'id': record.id,
                'model_name': record.model_name,
                'video_url': record.video_url
            })

        return jsonify({
            'success': True,
            'message': '查询成功',
            'data': result,
            'total_count': len(result)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'查询失败: {str(e)}'
        }), 500


# 2. 删除接口：根据model_name删除记录
@blue.route('/api/video', methods=['DELETE'])
def delete_video_by_model_name():
    """
    根据model_name删除videoModel表中的所有相关记录
    参数：model_name - 案例名称
    """
    try:
        from app.models import videoModel
        
        data = request.get_json() if request.is_json else request.form
        
        model_name = data.get('model_name')
        
        if not model_name:
            return jsonify({
                'success': False,
                'message': '缺少必要参数：model_name'
            }), 400

        # 查找要删除的记录
        video_records = videoModel.query.filter_by(model_name=model_name).all()
        
        if not video_records:
            return jsonify({
                'success': False,
                'message': f'未找到model_name为"{model_name}"的记录'
            }), 404

        # 保存删除前的信息用于返回
        deleted_count = len(video_records)
        deleted_info = []
        for record in video_records:
            deleted_info.append({
                'id': record.id,
                'model_name': record.model_name,
                'video_url': record.video_url
            })

        # 删除所有匹配的记录
        for record in video_records:
            db.session.delete(record)
        
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'删除成功，共删除{deleted_count}条记录',
            'deleted_records': deleted_info,
            'deleted_count': deleted_count
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }), 500


# 3. 添加接口：添加新的videoModel记录
@blue.route('/api/video', methods=['POST'])
def add_video_record():
    """
    添加新的videoModel记录
    参数：model_name, video_url
    """
    try:
        from app.models import videoModel
        
        data = request.get_json() if request.is_json else request.form
        
        # 获取参数
        model_name = data.get('model_name')
        video_url = data.get('video_url')

        # 参数验证
        if not all([model_name, video_url]):
            return jsonify({
                'success': False,
                'message': '缺少必要参数：model_name, video_url'
            }), 400

        # 创建新记录
        new_record = videoModel(
            model_name=model_name,
            video_url=video_url
        )

        # 添加到数据库
        db.session.add(new_record)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '添加成功',
            'data': {
                'id': new_record.id,
                'model_name': new_record.model_name,
                'video_url': new_record.video_url
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'添加失败: {str(e)}'
        }), 500


# ==================== 其他 ====================

# ==================== 微信上传文件接口 ====================
@blue.route('/api/upload', methods=['POST'])
def upload_file():
    """
    上传文件接口：接收文件本体，保存并返回文件URL
    """
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({'success': False, 'message': '未提供文件'}), 400

        filename = secure_filename(file.filename)

        # 确保 uploads 目录存在
        upload_folder = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        save_path = os.path.join(upload_folder, filename)
        file.save(save_path)

        file_url = f"http://127.0.0.1:5000/uploads/{filename}"

        return jsonify({'success': True, 'file_url': file_url}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'上传失败: {str(e)}'}), 500

# ==================== 文件访问接口 ====================
@blue.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    文件访问接口：提供上传文件的访问
    """
    try:
        upload_folder = os.path.join(os.getcwd(), 'uploads')
        return send_from_directory(upload_folder, filename)
    except Exception as e:
        return jsonify({'success': False, 'message': f'文件访问失败: {str(e)}'}), 404
