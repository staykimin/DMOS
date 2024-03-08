from kimin.core_server import Set_Server
from flask_cors import CORS
config_path = "kimin/cfg.min"

x = Set_Server(config_path)
server = x.Server()
CORS(server, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
	x.Routes(server)
	x.Run(server)