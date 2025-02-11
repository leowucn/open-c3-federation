import json

from flask import Blueprint, current_app, request
from werkzeug.local import LocalProxy

from .api import get_userinfo, get_endpoint_list, get_department
from .response import error_response_400, success_response, error_response_500

core = Blueprint("core", __name__)
logger = LocalProxy(lambda: current_app.logger)


@core.before_request
def before_request_func():
    current_app.logger.name = "user"


@core.route("/userinfo", methods=["GET"])
def get_userinfo_view():
    token = request.headers.get("token")

    if not token:
        return error_response_400("请在header中传递token")

    data = get_userinfo(token)
    if data is None:
        return error_response_400("无法根据指定邮箱获取到用户信息, 请确认邮箱是否填写正确")

    return success_response(data)


@core.route("/endpoints", methods=["GET"])
def get_endpoint_list_view():
    data = get_endpoint_list()
    return success_response(data)


@core.route("/department", methods=["GET"])
def get_department_view():
    email = request.args.get("email")

    if not email:
        return error_response_400("请传递email")

    data = get_department(email)
    if data is None:
        return error_response_400("无法根据指定邮箱获取到部门信息, 请确认邮箱是否填写正确")

    if data["code"] != 0:
        logger.error(f"get_department_view. 接口响应: {json.dumps(data)}")
        return error_response_500("内部处理出错")

    return success_response(data)
