#_*_ coding:utf-8 _*_
import paramiko

'''
仅做测试用，不执行其他动作
'''

#transport = paramiko.Transport(('127.0.0.1',65530))
#transport.connect(username='root',password='root')

ssh =paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key_file = '/root/.ssh/id_rsa'
key = paramiko.RSAKey.from_private_key(key_file) #载入私钥
ssh.load_system_host_keys()   #载入公钥
ssh.connect(hostname='127.0.0.1',port=65530,username='root',pkey=key)#使用私钥连接


stdin,stdout,stderr = ssh.exec_command('df -h')
result = stdout.read()
rs = result.decode()
print(rs)
ssh.close()
