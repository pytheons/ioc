from ioc.extra.command import Command

class StartCommand(Command):

    def __init__(self, flask):
        self.flask = flask

    def initialize(self, parser):
        parser.description = 'Start flask integrated server'
        parser.add_argument('--host', default='0.0.0.0', help="the host to bind the port")
        parser.add_argument('--port', default=5000, type=int, help="the port to listen")

    def execute(self, args, output):
        output.write("Starting flask...\n")

        self.flask.run(host=args.host, port=args.port, debug=args.debug)