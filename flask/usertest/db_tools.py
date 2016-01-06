#!flask/bin/python
import os.path
import imp
from migrate.versioning import api
from app import db
import config

def downgrade_database():
	downgradeSuccessful = False
	try:
		pv = api.db_version(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
		print('Current database version: ' + str(pv))
		print('Downgrading database...')
		api.downgrade(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO, pv - 1)
		nv = api.db_version(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
		if pv == nv:
			print 'Database version is at the minimum version.'
			downgradeSuccessful = False
		else:
			print('New database version: ' + str(nv))
			downgradeSuccessful = True
	except Exception as err:
		print 'Unable to downgrade database.'
		print err
	
	return downgradeSuccessful

def upgrade_database():
	upgradeSuccessful = False
	try:
		pv = api.db_version(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
		print('Current database version: ' + str(pv))
		print('Upgrading database...')
		api.upgrade(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
		nv = api.db_version(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
		if pv == nv:
			print 'Database version is at the maximum version.'
			upgradeSuccessful = False
		else:
			print('New database version: ' + str(nv))
			upgradeSuccessful = True
	except Exception as err:
		print 'Unable to upgrade database.'
		print err

	return upgradeSuccessful

def migrate_database():
	migrateSuccessful = False
	try:
		pv = api.db_version(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
		print('Current database version: ' + str(pv))
		print('Migrating database...')
		migration = config.SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (pv+1))
		tmp_module = imp.new_module('old_model')
		old_model = api.create_model(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
		exec(old_model, tmp_module.__dict__)
		script = api.make_update_script_for_model(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
		open(migration, "wt").write(script)
		api.upgrade(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
		nv = api.db_version(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
		print('New migration saved as ' + migration)
		print('Current database version: ' + str(nv))
		migrateSuccessful = True
	except Exception as err:
		print 'An error occurred while attempting to migrate database.'
		print err

	return migrateSuccessful

def create_database():
	createdSuccessfully = False
	if (os.path.exists(config.SQLALCHEMY_DATABASE_LOC)):
		print '\'%s\' already exists.' % config.SQLALCHEMY_DATABASE_LOC

	if (os.path.exists(config.SQLALCHEMY_MIGRATE_REPO)):
		print '\'%s\' already exists.' % config.SQLALCHEMY_MIGRATE_REPO

	try:
		db.create_all()
		if not os.path.exists(config.SQLALCHEMY_MIGRATE_REPO):
			api.create(config.SQLALCHEMY_MIGRATE_REPO, 'database repository')
			api.version_control(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO)
		else:
			api.version_control(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_MIGRATE_REPO, api.version(config.SQLALCHEMY_MIGRATE_REPO))
	except Exception as err:
		print 'An error occurred creating the database.'
		print err
		return createdSuccessfully
		
	if (os.path.exists(config.SQLALCHEMY_DATABASE_LOC)) and (os.path.exists(config.SQLALCHEMY_MIGRATE_REPO)):
		createdSuccessfully = True

	return createdSuccessfully