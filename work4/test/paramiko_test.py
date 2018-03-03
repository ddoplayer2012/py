#_*_ coding:utf-8 _*_
import paramiko


ssh =paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='127.0.0.1',port=65530,username='root',password='root')

stdin,stdout,stderr = ssh.exec_command('ls')
result = stdout.read()
ssh.close()
