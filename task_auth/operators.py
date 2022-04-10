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
Operator handling
"""
class Operator(ABC):
	operator = ""
	sender = "Django-app"
	msg = ""

	@abstractmethod
	def send_sms(self, phone_number):
		pass

	@abstractmethod
	def msg_text(self, otp_code):
		pass


class IrancellOperator(Operator):
	operator = "Irancell"
	
	def msg_text(self, otp_code):
		self.msg = f"Operator: {self.operator}, Sender: {self.sender}, OTP Code: {otp_code}"
	def send_sms(self, phone_number):
		print(f"Sending sms to {phone_number}")


class IrancellOperator(Operator):
	operator = "MCI"
	
	def msg_text(self, otp_code):
		self.msg = f"Operator: {self.operator}, Sender: {self.sender}, OTP Code: {otp_code}"
	def send_sms(self, phone_number):
		print(f"Sending sms to {phone_number}")

