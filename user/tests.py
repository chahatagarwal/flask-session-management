import pytest
from user import app, db
import json
import base64
from flask import Flask
from .models import  User

class Test_UserAPI:

	client  = app.test_client()
	
	@pytest.fixture(autouse=True, scope='session')
	def setUp(self):
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		db.create_all()
		yield db
		db.drop_all()

	def test_successful_registration(self):
		url = "/register"
		payload = "{\n\t\"username\": \"test01\",\n\t\"useremail\": \"user@test.com\",\n\t\"password\": \"test\"}"
		headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
		response = self.client.post(url, data=payload, headers=headers)
		assert response.status_code == 200
		assert response.json['Message'].strip() == 'Registration successful'
	
	def test_failed_registration(self):
		url = "/register"
		payload = "{\n\t\"username\": \"test01\",\n\t\"useremail\": \"user@test.com\",\n\t\"password\": \"test\"}"
		headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
		response = self.client.post(url, data=payload, headers=headers)
		assert response.status_code == 400
		assert response.json['Message'].strip() == 'Check the fields entered'

	def test_successful__user_login(self):
		valid_credentials = base64.b64encode(b'test01:test').decode('UTF-8')
		response = self.client.post('/login', headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		assert response.json['Message'].strip() == 'Login success'
		with self.client.session_transaction() as session:
			assert len(session)==2
			assert session['username'] == 'test01'
	
	def test_user_logout(self):
		url="/logout"
		response = self.client.post(url)
		assert response.status_code == 200
		assert response.json['Message'].strip() == 'Logout successful'
		with self.client.session_transaction() as session:
			assert len(session)==1
			
	def test_failed_user_login(self):
		valid_credentials = base64.b64encode(b'test01:test01').decode('UTF-8')
		response = self.client.post('/login', headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 400
		assert response.json['Message'].strip() == 'Could not verify'
		with self.client.session_transaction() as session:
			assert len(session)==1
	
	def test_failed_user_logout(self):
		url="/logout"
		response = self.client.post(url)
		assert response.status_code == 400
		assert response.json['Message'].strip() == 'Already logged out'
		with self.client.session_transaction() as session:
			assert len(session)==1