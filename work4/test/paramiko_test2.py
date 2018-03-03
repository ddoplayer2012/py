#_*_ coding:utf-8 _*_
import paramiko


transport = paramiko.Transport(('127.0.0.1',65530))
transport.connect(username='root',password='root')

ssh =paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect(hostname='127.0.0.1',port=65530,username='root',password='root')
ssh._transport = transport
stdin,stdout,stderr = ssh.exec_command('df -h')
result = stdout.read()
rs = result.decode()
print(rs)
ssh.close()
