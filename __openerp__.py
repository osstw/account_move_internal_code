# -*- coding: utf-8 -*-
{
    "name": "account_move_internal_code",
    "author": "糖葫芦(39181819@qq.com)",
    "depends": ["account", "account_accountant"],
    "data": ["views/account_move_views.xml",
             "views/internal_code.xml",
             "security/ir.model.access.csv"],
    "description": """
    当前版本 1.1

    更新记录

    版本 1.1，更新日期 2016-2-5

    1、model:internal code 加入权限设置，否则非administrator帐号不能正常生成编号。
    """
}
