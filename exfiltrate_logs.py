# Exfiltrate failed password attempts from our server.
# (i.e., failed_password_attempts.txt)

import paramiko

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        # for line in output:
        #     print(line.strip())
        with open('failed_password_attempts.txt', 'w') as f:
            f.write(str(output))

if __name__ == '__main__':
    import getpass
    user = input('Username: ')
    password = getpass.getpass()
    ip = input('Enter server IP: ')
    port = input('Enter port or <CR>: ') or 22
    cmd = input('Enter command or <CR>: ') # cat failed_password.txt
    ssh_command(ip, port, user, password, cmd)
