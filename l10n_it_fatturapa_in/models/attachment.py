# -*- coding: utf-8 -*-

import base64
from odoo import fields, models, api, _


class FatturaPAAttachmentIn(models.Model):
    _name = "fatturapa.attachment.in"
    _description = "E-bill import file"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']
    _order = 'id desc'

    ir_attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', required=True, ondelete="cascade")
    att_name = fields.Char(related='ir_attachment_id.name', store=True)
    in_invoice_ids = fields.One2many(
        'account.invoice', 'fatturapa_attachment_in_id',
        string="In Bills", readonly=True)
    xml_supplier_id = fields.Many2one(
        "res.partner", string="Supplier", compute="_compute_xml_data",
        store=True)
    invoices_number = fields.Integer(
        "Bills Number", compute="_compute_xml_data", store=True)
    invoices_total = fields.Float(
        "Bills Total", compute="_compute_xml_data", store=True,
        help="If specified by supplier, total amount of the document net of "
             "any discount and including tax charged to the buyer/ordered"
    )
    registered = fields.Boolean(
        "Registered", compute="_compute_registered", store=True)

    e_invoice_received_date = fields.Datetime(string='E-Bill Received Date')

    e_invoice_validation_error = fields.Boolean(
        compute='_compute_e_invoice_validation_error')

    e_invoice_validation_message = fields.Text(
        compute='_compute_e_invoice_validation_error')

    _sql_constraints = [(
        'ftpa_attachment_in_name_uniq',
        'unique(att_name)',
        'The name of the attachment must be unique!')]

    @api.depends('in_invoice_ids.e_invoice_validation_error')
    def _compute_e_invoice_validation_error(self):
        for att in self:
            bills_with_error = att.in_invoice_ids.filtered(
                lambda b: b.e_invoice_validation_error
            )
            if not bills_with_error:
                continue
            att.e_invoice_validation_error = True
            errors_message_template = u"{bill}:\n{errors}"
            error_messages = list()
            for bill in bills_with_error:
                error_messages.append(
                    errors_message_template.format(
                        bill=bill.display_name,
                        errors=bill.e_invoice_validation_message))
            att.e_invoice_validation_message = "\n\n".join(error_messages)

    @api.onchange('datas_fname')
    def onchagne_datas_fname(self):
        self.name = self.datas_fname

    def get_xml_string(self):
        return self.ir_attachment_id.get_xml_string()

    @api.multi
    @api.depends('ir_attachment_id.datas')
    def _compute_xml_data(self):
        for att in self:
            fatt = self.env['wizard.import.fatturapa'].get_invoice_obj(att)
            cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
            partner_id = self.env['wizard.import.fatturapa'].getCedPrest(
                cedentePrestatore)
            att.xml_supplier_id = partner_id
            att.invoices_number = len(fatt.FatturaElettronicaBody)
            att.invoices_total = 0
            for invoice_body in fatt.FatturaElettronicaBody:
                att.invoices_total += float(
                    invoice_body.DatiGenerali.DatiGeneraliDocumento.
                    ImportoTotaleDocumento or 0
                )

    @api.multi
    @api.depends('in_invoice_ids')
    def _compute_registered(self):
        for att in self:
            if (
                att.in_invoice_ids and
                len(att.in_invoice_ids) == att.invoices_number
            ):
                att.registered = True
            else:
                att.registered = False

    def extract_attachments(self, AttachmentsData, invoice_id):
        AttachModel = self.env['fatturapa.attachments']
        for attach in AttachmentsData:
            if not attach.NomeAttachment:
                name = _("Attachment without name")
            else:
                name = attach.NomeAttachment
            content = attach.Attachment
            _attach_dict = {
                'name': name,
                'datas': base64.b64encode(str(content)),
                'datas_fname': name,
                'description': attach.DescrizioneAttachment or '',
                'compression': attach.AlgoritmoCompressione or '',
                'format': attach.FormatoAttachment or '',
                'invoice_id': invoice_id,
            }
            AttachModel.create(_attach_dict)
