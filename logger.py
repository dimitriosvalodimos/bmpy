import logging


def init_logger():
    logging.basicConfig(
        filename="./bmpy.log", filemode="w", encoding="utf-8", level=logging.DEBUG
    )


def log(fn):
    logger = logging.getLogger()

    def func(*args, **kwargs):
        output = fn(*args, **kwargs)
        logger.info(f"{fn.__name__}, {args=}, {kwargs=} -> {output=}")
        return output

    return func
