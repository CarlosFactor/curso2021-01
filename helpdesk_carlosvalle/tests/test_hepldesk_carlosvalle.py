from odoo.tests import common           # Importamos de odoo
from odoo.exceptions import ValidationError

class TestHelpdeskAngelmoya(common.TransactionCase):
    # Creamos la funcion setUp, en la que preparamos los datos que quiero testear
    def setUp(self):
        super().setUp()

        # Me defino un ticket en el que voy a guardar un ticket que me he creado
        self.ticket = self.env["helpdesk.ticket"].create({
            'name': 'Test ticket'
        })
        # base.user_admin lo conseguimos yendo a usuarios y dando a view metada desde el insecto
        self.user_id = self.ref('base.user_admin')
    

    # Ahora ejecutamos metodos, que primero ejecutaran el setUp y luego lo 
    # que haya puesto
    # Creamos un metodo con el nombre que yo quiera 
    def test_01_ticket(self):
        """Test 01:
        Checking ticket name"""
        self.assertEqual(self.ticket.name, "Test ticket")
    

    def test_02_ticket(self):
        """Test 02:
        Checking ticket user and set it"""
        self.assertEqual(self.ticket.user_id, self.env['res.users'])
        self.ticket.user_id = self.user_id
        self.assertEqual(self.ticket.user_id.id, self.user_id)

    def test_03_ticket(self):
        """Test 03:
        Checking ticket name is not equal"""
        self.assertFalse(self.ticket.name == "asdfas ticketsdf ")

    def test_04_ticket(self):
        """Test 03:
        Checking time exception"""
        self.ticket.time = 4
        self.assertEqual(self.ticket.time, 4)
        self.ticket.time = 12
        self.assertEqual(self.ticket.time, 12)
        self.assertEqual(len(self.ticket.action_ids.ids), 2)

        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.ticket.time = -7