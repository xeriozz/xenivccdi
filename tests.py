#!/usr/bin/env python
import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Server


#Quelle: microblog https://github.com/miguelgrinberg/microblog
class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

#Quelle: microblog https://github.com/miguelgrinberg/microblog
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

#Eigenentwicklung: Eigenentwicklung auf Basis vom Microblog Code
    def test_user_creation(self):
        u = User(username='john', email='john@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()
        self.assertIsNotNone(u.id)
        self.assertEqual(u.username, 'john')
        self.assertEqual(u.email, 'john@example.com')
        self.assertTrue(u.check_password('password'))
#Eigenentwicklung: Eigenentwicklung auf Basis vom Microblog Code
    def test_unique_username_constraint(self):
        u1 = User(username='john', email='john@example.com')
        u1.set_password('password')
        db.session.add(u1)
        db.session.commit()
        u2 = User(username='john', email='john2@example.com')
        u2.set_password('password')
        db.session.add(u2)
        with self.assertRaises(Exception):
            db.session.commit()
#Eigenentwicklung: Eigenentwicklung auf Basis vom Microblog Code
    def test_unique_email_constraint(self):
        u1 = User(username='john', email='john@example.com')
        u1.set_password('password')
        db.session.add(u1)
        db.session.commit()
        u2 = User(username='john2', email='john@example.com')
        u2.set_password('password')
        db.session.add(u2)
        with self.assertRaises(Exception):
            db.session.commit()

#Eigenentwicklung: Eigenentwicklung auf Basis vom Microblog Code
    def test_server_creation(self):
        s = Server(servername='webserver', ip='192.168.1.100', os='Ubuntu')
        db.session.add(s)
        db.session.commit()
        self.assertIsNotNone(s.id)
        self.assertEqual(s.servername, 'webserver')
        self.assertEqual(s.ip, '192.168.1.100')
        self.assertEqual(s.os, 'Ubuntu')
#Eigenentwicklung: Eigenentwicklung auf Basis vom Microblog Code
    def test_unique_servername_constraint(self):
        s1 = Server(servername='webserver', ip='192.168.1.100', os='Ubuntu')
        db.session.add(s1)
        db.session.commit()
        s2 = Server(servername='webserver', ip='192.168.1.101', os='Windows')
        db.session.add(s2)
        with self.assertRaises(Exception):
            db.session.commit()
#Eigenentwicklung: Eigenentwicklung auf Basis vom Microblog Code
    def test_unique_ip_constraint(self):
        s1 = Server(servername='webserver1', ip='192.168.1.100', os='Ubuntu')
        db.session.add(s1)
        db.session.commit()
        s2 = Server(servername='webserver2', ip='192.168.1.100', os='Windows')
        db.session.add(s2)
        with self.assertRaises(Exception):
            db.session.commit()

#Eigenentwicklung: Eigenentwicklung auf Basis vom Microblog Code
    def test_server_modification(self):
        s = Server(servername='webserver', ip='192.168.1.100', os='Ubuntu')
        db.session.add(s)
        db.session.commit()
        s.servername = 'dbserver'
        s.ip = '192.168.1.101'
        s.os = 'Windows'
        db.session.commit()
        self.assertEqual(s.servername, 'dbserver')
        self.assertEqual(s.ip, '192.168.1.101')
        self.assertEqual(s.os, 'Windows')
#Eigenentwicklung: Eigenentwicklung auf Basis vom Microblog Code
    def test_server_deletion(self):
        s = Server(servername='webserver', ip='192.168.1.100', os='Ubuntu')
        db.session.add(s)
        db.session.commit()
        db.session.delete(s)
        db.session.commit()
        self.assertIsNone(Server.query.get(s.id))

if __name__ == '__main__':
    unittest.main(verbosity=2)
