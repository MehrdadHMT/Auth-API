from __future__ import annotations

import math
import random
import logging
from abc import ABC, abstractmethod
from django.core.cache import cache

logger = logging.getLogger(__name__)


def generate_otp():
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    otp = ""
    length = len(string)
    for i in range(6):
        otp += string[math.floor(random.random() * length)]

    return otp


"""
OTP handling
"""


class OTPCreator(ABC):
    otp_code = ""

    def __init__(self, otp_code):
        self.otp_code = otp_code

    @abstractmethod
    def factory_method(self):
        pass

    def operator_handler(self, ph_num):
        operator = self.factory_method()

        if operator.phone_number_validation(ph_num):
            cache.set(ph_num, self.otp_code, 60 * 4)
            operator.msg_text(self.otp_code)
            operator.send_sms(ph_num)

            return True
        else:
            return False


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
    operator_name = ""
    sender = "Django-app"
    msg = ""

    @abstractmethod
    def send_sms(self, ph_num):
        pass

    @abstractmethod
    def msg_text(self, otp_code):
        pass

    @abstractmethod
    def phone_number_validation(self, ph_num):
        pass


class IrancellOperator(Operator):
    def __init__(self):
        self.operator_name = "Irancell"

    def msg_text(self, otp_code):
        self.msg = f"Operator: {self.operator_name}, Sender: {self.sender}, OTP Code: {otp_code}"
        # return self.msg

    def send_sms(self, ph_num):
        # print(f"Sending sms to {ph_num}")
        logger.info(self.msg)

    def phone_number_validation(self, ph_num):
        try:
            if ph_num[-9] == '3':
                return True
            else:
                return False
        except TypeError:
            print("Phone number must be in 'string' format")


class MCIOperator(Operator):
    def __init__(self):
        self.operator_name = "MCI"

    def msg_text(self, otp_code):
        self.msg = f"Operator: {self.operator_name}, Sender: {self.sender}, OTP Code: {otp_code}"
        # return self.msg

    def send_sms(self, ph_num):
        # print(f"Sending sms to {ph_num}")
        logger.info(self.msg)

    def phone_number_validation(self, ph_num):
        try:
            if ph_num[-9] == '1':
                return True
            else:
                return False
        except TypeError:
            print("Phone number must be in 'string' format")


def client_code(ph_num: str) -> None:
    otp_code = generate_otp()
    otp_creator_list = OTPCreator.__subclasses__()
    for otp_cr in otp_creator_list:
        flag = otp_cr(otp_code).operator_handler(ph_num)

        if flag:
            break


if __name__ == "__main__":
    phone_number = "09126057206"
    client_code(phone_number)
