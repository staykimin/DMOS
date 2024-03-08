from kimin.core_db_web import Get_Conf
from flask import Flask
from flask.views import MethodView
class Set_Server:
	def __init__(kimin, config):
		kimin.path = config
		kimin.config = Get_Conf(path=config)
	
	def Routes(kimin, server):
		for i in kimin.config['routes']:
			if not i == "modul_name":
				modul = __import__(kimin.config['routes']['modul_name'])
				fungsi = kimin.config['routes'][i]['function']
				server.add_url_rule(
					kimin.config['routes'][i]['url'],
					view_func= getattr(modul, fungsi),
					methods=kimin.config['routes'][i]['methods']
					)
			
	def Server(kimin):
		server = Flask(
			__name__, 
			static_folder=kimin.config['server']['static_path'], 
			template_folder=kimin.config['server']['template_path'])
		
		if kimin.config['server']['template_auto_reload'] is True:
			server.jinja_env.auto_reload = True
			server.config['TEMPLATES_AUTO_RELOAD'] = True
		
		if kimin.config['server']['debug'] is True:
			server.config['DEBUG'] = True
		
		if 'secret_key' in kimin.config and not kimin.config['server']['secret_key'] is None:
			server.secret_key=kimin.config['server']['secret_key']
		
		if 'session_lifetime' in kimin.config and isinstance(kimin.config['server']['session_lifetime'], int):
			server.config["SESSION_PERMANENT"] = False
			server.config['PERMANENT_SESSION_LIFETIME'] =  datetime.timedelta(minutes=kimin.config['server']['session_lifetime'])
		
		return server
	
	def Run(kimin, server):
		server.run(host=kimin.config['server']['host'], debug=kimin.config['server']['debug'], port=kimin.config['server']['port'])