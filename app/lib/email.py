from django.core.mail import EmailMessage

class Email:


	def sendMail(title,body,frm,email):
		try:
			email = EmailMessage(title, body, frm,to=[email])
			email.send()
			return True
		except Exception as err:
			return False	