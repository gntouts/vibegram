
class Users:

	def __init__(self, user_id, first_name, last_name, avatar, phone_number, e_mail, password, created_account, is_active):
		self.user_id = user_id
		self.first_name = first_name
		self.last_name = last_name
		self.avatar = avatar
		self.phone_number = phone_number
		self.e_mail = e_mail
		self.password = password
		self.created_account = created_account
		self.is_active = is_active
		

	
class Messages:
	
	def __init__(self, message_id, sender_id, is_sent, date_time_sent, message_body, attachment):
		self.message_id = message_id
		self.sender_id = sender_id
		self.is_sent = is_sent
		self.date_time_sent = date_time_sent
		self.message_body = message_body
		self.attachment = attachment
	
	
class Receiving:
	
	def __init__(self, recipient_id, date_time_received, is_received, message_id):
		self.recipient_id = recipient_id
		self.date_time_received = date_time_received
		self.is_received = is_received
		self.message_id = message_id
		
	
class Friend:
	
	def __init__(self, friendship_id, friend1_id, friend2_id, date_added, friend_type):
		self.friendship_id = friendship_id
		self.friend1_id = friend1_id
		self.friend2_id = friend2_id
		self.date_added = date_added
		self.friend_type = friend_type