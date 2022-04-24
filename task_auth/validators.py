from django.core.validators import RegexValidator


otp_regex_validator = RegexValidator(regex=r"[0-9a-zA-Z]{6}", message="The OTP code must be in 6 characters, containing"
                                                                      "lowercase or uppercase letters or digits")

phone_regex_validator = RegexValidator(regex=r"^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$",
                                       message="Phone number must be entered in one of these formats: '09xxxxxxxxx',"
                                               " '989xxxxxxxxx', '+989xxxxxxxxx', '+9809xxxxxxxxx', '00989xxxxxxxxx',"
                                               "'0989xxxxxxxxx', '009809xxxxxxxxx'."
                                               " Up to 15 digits allowed.")