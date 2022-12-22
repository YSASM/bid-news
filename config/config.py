import logging
import os
import json


class Config(object):

    cfg = {}

    @classmethod
    def env(cls):
        return os.environ.get("ENV", "test")

    @classmethod
    def cluster(cls):
        return os.environ.get("CLUSTER", "")

    @classmethod
    def load(cls, env):
        if os.path.exists("./config/spider.%s.json" % str(env)):
            file = "./config/spider.%s.json" % str(env)
        elif os.path.exists("../config/spider.%s.json" % str(env)):
            file = "../config/spider.%s.json" % str(env)
        try:
            fd = open(file, "r")
            cfg = fd.read()
            logging.info(
                "env[%s] config[%s]",
                env,
                cfg,
            )
            cls.cfg = json.loads(cfg)
        except Exception as e:
            logging.error("config is load error: %s", str(e))

    @classmethod
    def get(cls):
        return cls.cfg

    @classmethod
    def get_val(cls, key, value):
        return cls.cfg.get(key, value)
