from logging.logger_wrapper import Logger


Logger.create_loggers(geneva=True,
                    namespace="n",
                    host="s",
                    port="a",
                    appId="a",
                    jobId="a")
Logger.info("Testing log wrapper")