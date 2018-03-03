
import hashlib

def hash(password):
    '''
    密码加密
    :param password:
    :return:
    '''
    m = hashlib.md5()
    m.update(password.encode("utf-8"))
    return m.hexdigest()