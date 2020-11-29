from datetime import datetime

LVL_INF = "INFO"
LVL_DBG = "DEBUG"
LVL_WRN = "WARNING"
LVL_ERR = "ERROR"


def info(message):
    log(LVL_INF, message)


def debug(message):
    log(LVL_DBG, message)


def warning(message):
    log(LVL_WRN, message)


def error(message):
    log(LVL_ERR, message)


def log(lvl, message):
    now = datetime.now()
    print("{} [{:>8}] {}".format(now, lvl, message))
