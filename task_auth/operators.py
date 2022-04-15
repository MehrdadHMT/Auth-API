from __future__ import annotations
from abc import ABC, abstractmethod

"""
OTP handling
"""
class OTPCreator(ABC):
	otp_code = ""
	@abstractmethod
	def factory_method(self):
		pass

	def send_otp(self):
		operator = self.factory_method()

		msg = f""

		return msg


class IrancellOTP(OTPCreator):
	def factory_method(self) -> IrancellOperator:
		return IrancellOperator()


class MCIOTP(OTPCreator):
	def factory_method(self) -> MCIOperator:
		return MCIOperator()


"""
Operators 
"""
class Operator(ABC):
	operator = ""
	sender = "Django-app"
	otp_code = ""
	msg = ""

	@abstractmethod
	def send_sms(self, phone_number):
		pass

	@abstractmethod
	def msg_text(self, otp_code):
		pass

	@abstractmethod
	def phone_number_operator(self, phone_number):
		pass


class IrancellOperator(Operator):
	def __init__(self):
		self.operator = "Irancell"
	
	def msg_text(self, otp_code):
		self.msg = f"Operator: {self.operator}, Sender: {self.sender}, OTP Code: {otp_code}"
		return self.msg

	def send_sms(self, phone_number):
		print(f"Sending sms to {phone_number}")

	def phone_number_operator(self, phone_number):
		try:
			if phone_number[2] == '3':
				return True
			else:
				return False
		except TypeError:
			print("Phone number must be in 'string' format")


class MCIOperator(Operator):
	def __init__(self):
		self.operator = "MCI"
	
	def msg_text(self, otp_code):
		self.msg = f"Operator: {self.operator}, Sender: {self.sender}, OTP Code: {otp_code}"
		return self.msg

	def send_sms(self, phone_number):
		print(f"Sending sms to {phone_number}")

	def phone_number_operator(self, phone_number):
		try:
			if phone_number[2] == '1':
				return True
			else:
				return False
		except TypeError:
			print("Phone number must be in 'string' format")

