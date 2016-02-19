# _*_ coding: utf-8 _*_
from openerp import models, fields, api


class AccountVoucher(models.Model):
    _inherit = "account.voucher"

    cus_code_for_move = fields.Char(readonly=True, copy=False)

    @api.multi
    def update_cus_code_for_move(self, date=None):
        self.ensure_one()
        InternalCode = self.env["account_move_internal_code.internal_code"]
        if self.cus_code_for_move:
            InternalCode.recover_if_biggest(self.cus_code_for_move)
        key = InternalCode.generate_key_from_date(date or self.date)
        self.cus_code_for_move = InternalCode.next_code_by_key(key)
        return True

    @api.model
    def account_move_get(self, voucher_id):
        result = super(AccountVoucher, self).account_move_get(voucher_id)
        voucher = self.browse(voucher_id)
        voucher.ensure_one()
        if not voucher.cus_code_for_move:
            voucher.update_cus_code_for_move()
        result["customize_internal_code"] = voucher.cus_code_for_move
        result["internal_code_type"] = "voucher"
        return result

    @api.multi
    def write(self, vals):
        date = vals.get("date", None)
        if date:
            for voucher in self:
                if voucher.date and voucher.date != date:
                    voucher.update_cus_code_for_move(date)
                    if voucher.move_id:
                        voucher.move_id.customize_internal_code = voucher.cus_code_for_move
        return super(AccountVoucher, self).write(vals)
