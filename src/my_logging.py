from datetime import datetime

LVL_DBG = {"name": "DEBUG", "value": 0}
LVL_WRN = {"name": "WARNING", "value": 1}
LVL_INF = {"name": "INFO", "value": 2}
LVL_ERR = {"name": "ERROR", "value": 3}


def log_level_from_name(level_name):
    if level_name is None:
        return None

    input_level = str(level_name).strip().upper()
    if input_level == LVL_DBG["name"]:
        return LVL_DBG
    elif input_level == LVL_WRN["name"]:
        return LVL_WRN
    elif input_level == LVL_INF["name"]:
        return LVL_INF
    elif input_level == LVL_ERR["name"]:
        return LVL_ERR
    else:
        raise Exception("No valid logging level provided: {}".format(level_name))


class Logger:

    def __init__(self, log_lvl):
        self.lvl = log_lvl if log_lvl is not None else LVL_INF

    def info(self, message):
        self._log(LVL_INF, message)

    def debug(self, message):
        self._log(LVL_DBG, message)

    def warning(self, message):
        self._log(LVL_WRN, message)

    def error(self, message):
        self._log(LVL_ERR, message)

    def _log(self, lvl, message):
        if lvl["value"] >= self.lvl["value"]:
            now = datetime.now()
            print("{} [{:>8}] {}".format(now, lvl["name"], message))
