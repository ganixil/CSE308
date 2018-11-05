import datetime

# class for containing available date information
class DateObject():
	def __init__(self, date, canEmail, dateId):
		self.date = date
		self.canEmail = canEmail
		self.dateId = dateId

# class for modeling assignment mapping to dates
class assignmentMapping():
	def __init__(self, date, canEmail, dateId, assignment):
		self.date = date
		self.canEmail = canEmail
		self.dateId = dateId
		self.assignment = assignment