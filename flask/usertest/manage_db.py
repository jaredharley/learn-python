#!flask/bin/python
import sys
from getpass import getpass
from sqlalchemy import exc
from flask import app
from app import bcrypt, db
from app.models import User

import db_tools
import utils as u

def DisplayUserList():
	userList = User.query.all()
	if not userList:
		print ''
		print u.colorText('ERROR: Unable to read users from database.', 'red')
		print 'This could be because of a database communication failure or there'
		print 'are no users in the database.'
		print ''
		return
	print ''
	print ' ID\tEmail\t\tLast logon\tCreated'
	print ' ----\t--------------\t------------\t---------'
	for user in userList:
		print " {0}\t{1}\t\t{2}\t{3}".format(user.id, user.email, user.last_logon, user.created)
	print ''
	return

def ListAllUsers():
	u.ClearScreen()
	print ''
	print u.colorText('LIST ALL USERS IN DATABASE', 'green')
	DisplayUserList()
	raw_input('Press '+u.colorText('[return]','yellow')+' to go back to the main screen')
	return

def AddNewUser():
	u.ClearScreen()
	print ''
	print u.colorText('CREATE A NEW USER', 'green')
	creatingUser = True
	while creatingUser:
		print ''
		print 'Enter the email address for the new user or '+u.colorText('[Q]','yellow') + ' to go back:'
		email = raw_input('')

		if (email == 'q') or (email == 'Q'):
			return

		if not email:
			print u.colorText('Email address cannot be blank.','red')
			continue

		passwordGood = False
		while not passwordGood:
			try:
				password = getpass('Enter a password: ')
				assert password == getpass('Password (again): ')
				if not password:
					print u.colorText('Password cannot be blank.','red')
					continue
			except AssertionError as err:
				print u.colorText('Passwords do not match.','red')
				continue
			passwordGood = True

		print 'User {0} is about to be created.'.format(u.colorText(email, 'yellow'))
		confirm = raw_input('Do you want to create this user? ' + u.colorText('(y/n)','yellow') + ': ')

		if (confirm == 'y') or (confirm == 'Y'):
			user = User(email=email, password=bcrypt.generate_password_hash(password))
			db.session.add(user)
			try:
				db.session.commit()
				print u.colorText('User ','green')+u.colorText(email,'yellow')+u.colorText(' was created.','green')
			except exc.SQLAlchemyError as err:
				db.session.rollback()
				print u.colorText('Email address already exists.','red')
				print u.colorText('User was not created.','red')
				print ''

		continue
	return

def DeleteUser():
	u.ClearScreen()
	print ''
	print u.colorText('DELETE AN EXISTING USER', 'green')
	DisplayUserList()
	deletingUser = True
	while deletingUser:
		idToDelete = raw_input('Enter the ID of the user to delete or '+u.colorText('[Q]','yellow') + ' to go back: ')
		if (idToDelete == 'q') or (idToDelete == 'Q'):
			return
		if not idToDelete:
			print u.colorText('ID to delete cannot be blank.', 'red')
			print ''
			continue
		try:
			idToDelete = int(idToDelete)
		except ValueError as err:
			print u.colorText('You must enter a valid ID value.', 'red')
			continue

		userToDelete = User.query.get(idToDelete)
		if not userToDelete:
			print u.colorText('There is no user with an ID of \'%d\'' % idToDelete, 'red')
			continue

		print u.colorText('You are about to delete ','red') + u.colorText(userToDelete.email,'yellow')
		print u.colorText('This action cannot be undone','red')
		deleteUser = raw_input('Do you want to delete this user? '+u.colorText('(y/n)','yellow') + ': ')
		if (deleteUser == 'y') or (deleteUser == 'Y'):
			db.session.delete(userToDelete)
			try:
				db.session.commit()
				print u.colorText('User ','green')+u.colorText(userToDelete.email,'yellow')+u.colorText(' was deleted.','green')
			except exc.SQLAlchemyError as err:
				db.session.rollback()
				print u.colorText('An error occurred while trying to delete the user.','red')
				print u.colorText('User was not deleted.','red')
				print err
				print ''

		continue

def ChangePassword():
	u.ClearScreen()
	print ''
	print u.colorText('CHANGE USER\'S PASSWORD','green')
	changingPassword = True
	DisplayUserList()
	while changingPassword:
		idToChange = raw_input('Enter the ID of the user to change password or '+u.colorText('[Q]','yellow') + ' to go back: ')
		if (idToChange == 'q') or (idToChange == 'Q'):
			return

		if not idToChange:
			print u.colorText('ID to change password cannot be blank.', 'red')
			print ''
			continue
		try:
			idToChange = int(idToChange)
		except ValueError as err:
			print u.colorText('You must enter a valid ID value.', 'red')
			continue

		userToChange = User.query.get(idToChange)
		if not userToChange:
			print u.colorText('There is no user with an ID of \'%d\'' % idToChange, 'red')
			continue

		print u.colorText('You are about to change the password for the user \'%s\'' % userToChange.email,'yellow')
		changeUser = raw_input('Do you want to change this user\'s password? '+u.colorText('(y/n)','yellow') + ': ')
		if (changeUser == 'y') or (changeUser == 'Y'):
			passwordGood = False
			while not passwordGood:
				try:
					password = getpass('Enter the new password:')
					assert password == getpass('Password (again):')
					if not password:
						print u.colorText('Password cannot be blank.','red')
						continue
				except AssertionError as err:
					print u.colorText('Passwords do not match.','red')
					continue
				passwordGood = True

			userToChange.password = bcrypt.generate_password_hash(password)
			try:
				db.session.commit()
				print u.colorText('Password for user ','green')+u.colorText(userToChange.email,'yellow')+u.colorText(' was changed.','green')
			except exc.SQLAlchemyError as err:
				db.session.rollback()
				print u.colorText('An error occurred while trying to update the user\'s password.','red')
				print u.colorText('User\'s password was not updated.','red')
				print err
				print ''

		continue

def VerifyCredentials():
	u.ClearScreen()
	print ''
	print u.colorText('VERIFY USER CREDENTIALS','green')
	verifingCreds = True
	while verifingCreds:
		print ''
		testEmail = raw_input('Enter email address or '+u.colorText('[Q]','yellow') + ' to go back: ')
		if (testEmail == 'q') or (testEmail == 'Q'):
			return
		if not testEmail:
			print u.colorText('Email address cannot be blank.','red')

		userToVerify = User.query.filter_by(email=testEmail).first()
		if not userToVerify:
			print u.colorText('There is no user with an email address of \'%s\'' % testEmail, 'red')
			continue

		testPassword = getpass('Enter password: ')

		if bcrypt.check_password_hash(userToVerify.password, testPassword):
			print u.colorText('Credentials are correct.','green')
		else:
			print u.colorText('Credentials are not correct.','red')

def CreateDatabase():
	u.ClearScreen()
	print ''
	print u.colorText('CREATE DATABASE','green')
	print 'This function will create a new database based off the Models script.'
	print ''
	shouldCreate = raw_input('Would you like to create the database? '+u.colorText('(y/n)','yellow') + ': ')

	if (shouldCreate == 'y') or (shouldCreate == 'Y'):
		if db_tools.create_database():
			print u.colorText('Database was successfully created.','green')
		else:
			print u.colorText('Database creation failed.','red')
	print ''
	raw_input('Press '+u.colorText('[return]','yellow')+' to go back to the main screen')
	return

def MigrateDatabase():
	u.ClearScreen()
	print ''
	print u.colorText('MIGRATE DATABASE','green')
	print 'This function will migrate the database to the next version.'
	print ''
	db_tools.migrate_database()
	shouldMigrate = raw_input('Would you like to migrate the database? '+u.colorText('(y/n)','yellow') + ': ')

	if (shouldMigrate == 'y') or (shouldMigrate == 'Y'):
		if db_tools.migrate_database():
			print u.colorText('Database was successfully migrated.','green')
		else:
			print u.colorText('Database migration failed.','red')
	print ''
	raw_input('Press '+u.colorText('[return]','yellow')+' to go back to the main screen')
	return

def UpgradeDowngradeDatabase():
	u.ClearScreen()
	print ''
	print u.colorText('UPGRADE OR DOWNGRADE DATABASE','green')
	optioning = True
	while optioning:
		print ''
		print u.colorText(' [U]','yellow') + ' Upgrade the database'
		print u.colorText(' [D]','yellow') + ' Downgrade the database'
		print u.colorText(' [Q]','yellow') + ' Go back to main menu'
		print ''
		option = raw_input('What would you like to do? ')

		if (option == 'u') or (option == 'U'):
			if db_tools.upgrade_database():
				print u.colorText('Database was successfully upgraded.','green')
			else:
				print u.colorText('Database upgrade failed.','red')
			optioning = False
		elif (option == 'd') or (option == 'D'):
			if db_tools.downgrade_database():
				print u.colorText('Database was successfully downgraded.','green')
			else:
				print u.colorText('Database downgrade failed.','red')
			optioning = False
		elif (option == 'q') or (option == 'Q'):
			return
		else:
			print u.colorText('Please select a valid option.', 'red')
			continue
	print ''
	raw_input('Press '+u.colorText('[return]','yellow')+' to go back to the main screen')
	return

def main():
	db.metadata.create_all(db.engine)
	showError = False
	while True:
		u.ClearScreen()
		print ''
		print u.colorText('USER AND DATABASE MANAGEMENT','green')
		print ''
		print u.colorText(' [1]','yellow') + ' List all users'
		print u.colorText(' [2]','yellow') + ' Create new user'
		print u.colorText(' [3]','yellow') + ' Delete existing user'
		print u.colorText(' [4]','yellow') + ' Change user\'s password'
		print u.colorText(' [5]','yellow') + ' Verify user credentials'
		print ''
		print u.colorText(' [6]','yellow') + ' Run database creation script'
		print u.colorText(' [7]','yellow') + ' Run database migration script'
		print u.colorText(' [8]','yellow') + ' Upgrade or downgrade database'
		print ''
		print u.colorText(' [Q]','yellow') + ' Quit'
		print ' '
		if showError:
			print u.colorText('Please enter a valid selection.','red')
			showError = False
		print 'What would you like to do? ',
		selection = raw_input()
		
		if selection == '1':
			ListAllUsers()
		elif selection == '2':
			AddNewUser()
		elif selection == '3':
			DeleteUser()
		elif selection == '4':
			ChangePassword()
		elif selection == '5':
			VerifyCredentials()
		elif selection == '6':
			CreateDatabase()
		elif selection == '7':
			MigrateDatabase()
		elif selection == '8':
			UpgradeDowngradeDatabase()
		elif (selection == 'Q') or (selection == 'q'):
			u.ClearScreen()
			sys.exit()
		else:
			showError = True

if __name__ == '__main__':
	main()