from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Doctor,Patient
from hospital.models import Hospital,Appointment
from .serializers import *
from hospital.serializers import HospitalSerializer,AppointmentSerializer
from web3 import Web3
import io
import json


class RegisterView(APIView):

	def post(self, request, format=None):
		username = request.data["username"]
		first_name = request.data["first_name"]
		last_name = request.data["last_name"]
		password = request.data["password"]
		cpassword = request.data["cpassword"]

		if password == cpassword:
			try:
				user = User.objects.create(username=username, first_name=first_name,
											last_name=last_name)
				
				user.set_password(password)
				user.save()

				token, created = Token.objects.get_or_create(user=user)

				userData = UserSerializer(user)
				tokenData = TokenSerializer(token)

				return Response({"user":userData.data,"token":tokenData.data}, status=status.HTTP_200_OK)
			except:
				return Response({"detail":"Error creating user."})	
		else:
			return Response({"detail":"Passwords don't match."})

		

class LoginView(APIView):
	"""
	Login with token auth
	"""

	def post(self, request, format=None):
		username = request.data["username"]
		password = request.data["password"]

		user = authenticate(username=username,password=password)

		token, created = Token.objects.get_or_create(user=user)
		tokenData = TokenSerializer(token)

		return Response(tokenData.data)

class DoctorRegisterView(APIView):
	
	def post(self, request, format=None):
		contact = request.data.get("contact", None)
		profile_pic = request.data.get("profile_pic", None)
		age = request.data("age", None)
		gender = request.data("gender", None)
		email = request.data.get("email", None)
		unique_id = request.data("unique_id",None)
		address = request.data("address", None)
		pincode = request.data("pincode", None)
		city = request.data("city", None)
		skill_data = request.data.get("skill", None)
		hospital_id = request.data("hospital_id", None)

		hospital_obj = Hospital.objects.get(id=hospital_id)
		city_obj = City.objects.get(city=city)

		doctor = Doctor.objects.create(user = request.healthy_user, contact = contact, profile_pic = profile_pic,
										age = age, gender =  gender, email = email, unique_id = unique_id,
										address = address, pincode = pincode, city = city_obj, hospital = hospital_obj)
		
		skills = []
		for skill in skill_data:
			skill_obj = Specialization.objects.create_or_get(field_name=skill)
			doctor.skill.add(skill_obj)
		doctor.save()

		return Response(doctor)


class PatientRegisterView(APIView):

	def post(self, request, format=None):
		contact = request.data["contact"]
		age = request.data["age"]
		address = request.data["address"]
		pincode = request.data["pincode"]
		city = request.data["city"]
		unique_id = request.data["unique_id"]

		city_obj = City.objects.get(city=city)

		patient = Patient.objects.create(user = request.healthy_user, contact = contact, age = age,
										address = address, pincode = pincode, city = city_obj,
										unique_id = unique_id) 

class DoctorView(APIView):

	def get(self, request, format=None):
		user = request.healthy_user
		doctor_details = DoctorSerializer(user.doctor)
		appointments = user.doctor.my_appointments.all()
		appointments = AppointmentSerializer(appointments, many=True)
		return Response({"doctor_details":doctor_details.data, "appointments":appointments.data}, status.HTTP_200_OK)

class AddMedicalRecordView(APIView):

	def post(self, request, formt=None):

		hospname =  request.data["hospname"]
		docname = request.data["docname"]
		docspeciality = request.data["docspeciality"]
		address = request.data["address"]
		date = request.data["date"]
		patname = request.data["patname"]
		age = request.data["age"]
		gender = request.data["gender"]
		disease = request.data["disease"]
		medicines = request.data["medicines"]

		"""
		Blockchain on duty
		"""
		w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))       #Creating Instance of web3 object
		with open("contracts/data.json", 'r') as f:
			datastore = json.load(f)
			abi = datastore["abi"]
			contract_address = datastore["contract_address"]

		w3.eth.defaultAccount = w3.eth.accounts[1]                      #Selecting an account with which trancsactions would happen
		RecordInstance = w3.eth.contract(address=contract_address, abi=abi)   #Getting the instance of deployed contract using ABI and address 

		#Saving data to Blockchain
		RecordInstance.functions.addData(hospname, docname , docspeciality, address,
		date, patname, age, gender, disease, medicines).transact()
		block_id = RecordInstance.functions.recordCount().call()

		print("Data stored in Blockchain successfully, id = ", block_id)
		
		print("Fetching Data ...")
		Data = RecordInstance.functions.showData(int(block_id)).call()
		print(Data)

