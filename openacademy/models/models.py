# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time 
   
def get_uid(self, *a):
#si se desea ver que nomas tiene la variable usar pdb
#    import pdb; pdb.set_trace()
    return self.env.uid

class Course(models.Model):
     _name = 'openacademy.course'

     name = fields.Char(string="Title", required=True)
     description = fields.Text()
#     responsible_id = fields.Many2one('res.users', string="Responsible",
#			index=True, ondelete='set null')
#lamdba self, a*:self.env.uid toma por defecto el usuario por defecto
     responsible_id = fields.Many2one(
     'res.users', string="Responsible",
     index=True, ondelete='set null', 
     #default=lambda self, *a: self.env.uid)
     default=get_uid)
     session_ids = fields.One2many('openacademy.session', 'course_id')

class Session(models.Model):
     _name = 'openacademy.session'

     name = fields.Char(required=True)
# fields.Data declara un campo de tipo fecha y desplega un calendario
#     start_date = fields.Date()
# default=fields.Date.today -> por defecto muestra la fecha actual
     start_date = fields.Date(default=fields.Date.today)
# lambda *a: quiere decir que se le puede pasar cualquier parametro 
#y lo procesará, sin embargo esta es una manera muy técnica
#     datetime_test = fields.Datetime(default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
# odoo tiene su propia manera para que no nos compliquemos
     datetime_test = fields.Datetime(default=fields.Datetime.now)
     duration = fields.Float(digits=(6, 2), help="Duration in days")
     seats = fields.Integer(string="Number of seats")
     instructor_id = fields.Many2one('res.partner', string='Instructor'
     , domain=['|', ('instructor', '=', True),
     ('category_id.name', 'ilike', 'Teacher')])
     course_id = fields.Many2one('openacademy.course', ondelete='cascade',
     string="Course", required=True)
     
     attendee_ids = fields.Many2many('res.partner', string="Attendees")
     taken_seats = fields.Float(compute='_taken_seats')
#   campo reservado active, siempre debe ser decclarado como boolean
#   por defecto será true, es decir que al crear una sesión estará activa
     active = fields.Boolean(default=True)

     @api.depends('seats','attendee_ids')
     def _taken_seats(self):
#        import pdb;pdb.set_trace()
#        for record in self:
#            if not record.seats: record.taken_seats = 0.0  
#            else: record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats
         for record in self.filtered(lambda r: r.seats):
             record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats
