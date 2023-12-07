import yaml

from sshcheckers import ssh_checkout, upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def deploy():
    res = []
    upload_files(f"{data.get('ip')}",
                 f"{data.get('user')}",
                 f"{data.get('password')}",
                 f"{data.get('folder_7z')}{data.get('filename')}.deb",
                 f"{data.get('folder_server')}{data.get('filename')}.deb")
    res.append(ssh_checkout(f"{data.get('ip')}",
                            f"{data.get('user')}",
                            f"{data.get('password')}",
                            f"echo {data.get('password')} | sudo -S dpkg -i {data.get('folder_server')}{data.get('filename')}.deb",
                            'Настраивается пакет'))
    res.append(ssh_checkout(f"{data.get('ip')}",
                            f"{data.get('user')}",
                            f"{data.get('password')}",
                            f"echo {data.get('password')} | sudo -S dpkg -s {data.get('filename')}",
                            'Status: install ok installed'))
    return all(res)


if deploy():
    print('Deploy is ok')
else:
    print('Deploy is failed')
