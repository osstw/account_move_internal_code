# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    customize_internal_code = fields.Char(readonly=True, copy=False)
    internal_code_type = fields.Selection([("invoice", "invoice"), ("voucher", "voucher"), ("manual", "manual")])

    @api.model
    def create(self, vals):
        if not vals.get("customize_internal_code", None):  # 说明当前是手动创建
            InternalCode = self.env["account_move_internal_code.internal_code"]
            key = InternalCode.generate_key_from_date(vals.get("date", None))
            cus_code = InternalCode.next_code_by_key(key)
            vals["customize_internal_code"] = cus_code
        return super(AccountMove, self).create(vals)

    @api.multi
    def unlink(self):
        InternalCode = self.env["account_move_internal_code.internal_code"]
        for move in self:
            if move.internal_code_type not in ("invoice", "voucher") and move.customize_internal_code:
                InternalCode.recover_if_biggest(move.customize_internal_code)
        return super(AccountMove, self).unlink()

    @api.multi
    def write(self, vals):
        vals_date = vals.get("date", None)
        if vals_date:
            InternalCode = self.env["account_move_internal_code.internal_code"]
            for move in self:
                if move.date and move.date != vals_date and move.customize_internal_code:
                    InternalCode.recover_if_biggest(move.customize_internal_code)
                key = InternalCode.generate_key_from_date(vals_date)
                cus_code = InternalCode.next_code_by_key(key)
                vals["customize_internal_code"] = cus_code
        return super(AccountMove, self).write(vals)
