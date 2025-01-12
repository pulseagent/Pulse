import logging


class Log(object):
    """"""
    _executed = False

    @staticmethod
    def init():
        """"""
        if Log._executed:
            return

        fmt = f"%(asctime)s [%(levelname)s] %(filename)s:%(funcName)s:%(lineno)s - %(message)s"

        formatter = logging.Formatter(
            fmt=fmt,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        logging.basicConfig(level=logging.INFO)
        logging.getLogger().handlers[0].setFormatter(formatter)
