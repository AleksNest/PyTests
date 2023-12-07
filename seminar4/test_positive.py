import yaml

from sshcheckers import ssh_checkout, upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    #  развертывание пакета на сервере, проверка успешной установки на сервере
    def test_deploy(self):
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
        assert all(res)

    # тестирование архиватора на создание архива на удаленном сервере
    def test_step1(self, make_folders, make_files):
        res = []
        res.append(ssh_checkout(f"{data.get('ip')}", f"{data.get('user')}", f"{data.get('password')}",
                                f"cd {data['folder_in']}; 7z a -t{data['type']} {data['folder_out']}/arx2",
                                f"{data['valid']}"))
        res.append(ssh_checkout('0.0.0.0', f"{data['user']}", f"{data['password']}",
                                f"cd {data['folder_out']}; ls", f"arx2.{data['type']}"))
        assert all(res)

    #  тестирование архиватора на извлечение из архива файлов в указанную папку
    def test_step2(self, make_files):
        res = []
        res.append(ssh_checkout(f"{data.get('ip')}", f"{data.get('user')}", f"{data.get('password')}",
                                f"cd {data.get('folder_out')}; 7z e arx2.{data.get('type')} -o{data.get('folder_ext')} -y",
                                f"{data.get('valid')}"))
        res.append(ssh_checkout(f"{data.get('ip')}", f"{data.get('user')}", f"{data.get('password')}",
                                "cd {}; ls".format(data.get('folder_ext')), make_files[0]))
        assert all(res)

    

    #  тестирование архиватора на создание архива с определенным расширением ключ -t
    def test_step6(self):
        assert ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                            f"cd {data['folder_out']}; 7z t arx2.{data['type']}",
                            f"{data['valid']}"), "test6 FAIL"

    # тестирование на Обновление файлов в архиве ключ -v
    def test_step7(self):
        assert ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                            f"cd {data['folder_in']}; 7z u {data['folder_out']}/arx2.{data['type']}",
                            f"{data['valid']}"), "test7 FAIL"

    # тестирование на удаление файлов в архиве ключ -d
    def test_step8(self):
        assert ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                            f"cd {data['folder_out']}; 7z d arx2.{data['type']}",
                            f"{data['valid']}"), "test8 FAIL"
    # тестирование на создание архива в
    def test_step5(self, make_files, make_sub_folder):
        result2 = ssh_checkout(f"{data['ip']}",
                               f"{data['user']}",
                               f"{data['password']}",
                               f"cd {data['folder_in']}; 7z a -t{data['type']} {data['folder_out']}/arx2",
                               f"{data['valid']}")
        result1 = ssh_checkout(f"{data['ip']}",
                               f"{data['user']}",
                               f"{data['password']}",
                               f"cd {data['folder_out']}; 7z d arx2.{data['type']}",
                               f"{data['valid']}")
        assert result1 and result2, "test5 FAIL"

# удаление пакета на сервере
    def test_delete(self):
        assert ssh_checkout(f"{data['ip']}",
                            f"{data['user']}",
                            f"{data['password']}",
                            f"echo {data.get('password')} | sudo -S dpkg -r {data.get('filename')}",
                            "Удаляется")
