import logging


def get_logger(name: str = __name__):
	"""快速取得設定好格式的 logger。

	回傳 python logging 的 logger 實例。
	"""
	logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
	return logging.getLogger(name)

