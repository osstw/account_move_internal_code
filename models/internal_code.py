# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.fields import Date

CODE_FORMAT = "%s%03d"


class InternalCode(models.Model):
    _name = "account_move_internal_code.internal_code"
    _rec_name = "key"

    key = fields.Char()
    next_number = fields.Integer(string="Last number", default=0,
                                 help="This is the lasted number used.When a new one is needed,returns +1")

    @api.model
    def generate_key_from_date(self, date_str=None):
        if date_str:
            date = Date.from_string(date_str)
            key = "%04d%02d%02d" % (date.year, date.month, date.day)
            return key

    @api.model
    def next_code_by_key(self, key=None):
        if key:
            internal_code = self.search([("key", "=", key)])
            if not internal_code:
                internal_code = self.create({"key": key})
            internal_code.ensure_one()

            return internal_code.next_code()

    @api.multi
    def next_code(self):
        self.ensure_one()
        self.inc_number()
        return self.code()

    @api.multi
    def code(self):
        self.ensure_one()
        return CODE_FORMAT % (self.key, self.next_number)

    @api.multi
    def dec_number(self):
        self.ensure_one()
        self.next_number -= 1
        return True

    @api.multi
    def inc_number(self):
        self.ensure_one()
        self.next_number += 1
        return True

    @api.multi
    def recover_if_biggest(self, code):
        key = code[0:8]
        internal_code = self.search([("key", "=", key)])
        internal_code.ensure_one()
        cur_code = internal_code.code()
        if code == cur_code:
            internal_code.dec_number()
        return True
