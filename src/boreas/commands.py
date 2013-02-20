'''
Created on 20-02-2013

@author: karol
'''
def boreas():
    from tornado.options import define, options    
    from boreas import server
    
    define("config", help="Configuration module", type=str)
    
    define("debug", default=True, help="Enable debugging urls", type=bool)
    define("api_port", default=8001, help="API port", type=int)
    define("api_host", default='127.0.0.1', help="API host", type=str)
    define("ws_port", default=8002, help="Websocket port", type=int)
    define("ws_host", default='127.0.0.1', help="Websocket host", type=str)
    define("token_provider", default='boreas.utils.tokens:no_tokens', help="Function providing initial tokens", type=str)
    
    options.parse_command_line()
    
    if options.config is None:
        # assume boreas.conf in working directory
        conf_file = 'boreas.conf'
        try:
            options.parse_config_file(conf_file)
        except IOError:
            pass # just use defaults
    else:
        conf_file = options.config
        options.parse_config_file(conf_file)
    
    server.run(options)