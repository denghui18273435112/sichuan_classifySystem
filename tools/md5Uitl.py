import  hashlib
def get_md5(MD5_text):
    """
    :param MD5_text: 需要MD5加密的内容
    :return:
    """
    return hashlib.md5(MD5_text.encode(encoding="utf-8")).hexdigest()


