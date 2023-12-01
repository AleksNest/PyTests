from task_1 import checkout, crc
import pytest



folder_in = '/home/alex/folder_in'
folder_out = '/home/alex/folder_out'
folder_ex = '/home/alex/folder_ex'
home = '/home/alex'


#тестирование  добавления файлов в ахив 7
def test_step_1():
    #assert checkout("cd /home/alex/folder_in; 7z a /home/alex/folder_out/archive_1", "Everything is Ok"), print("test_1 is FAILED")
    assert checkout(f"cd {folder_in}; 7z a {folder_out}/archive_1", "Everything is Ok"), print("test_1 is FAILED")

# тестирование  удаления всех файлов из архива
def test_step_2():
    assert checkout(f"cd {folder_out}; 7z d archive_1", 'Everything is Ok'), print("test_2 is FAILED")


 # тестирование  извлечения архива  в текущую папку
def test_step_3():
    assert checkout(f"cd {folder_in}; 7z a {folder_out}/archive_2; cd {folder_out}; 7z e archive_2.7z", 'Everything is Ok'), print("test_3 is FAILED")


# тестирование  извлечения архива  в указанную папку
def test_step_4():
    assert checkout(f"cd {folder_out}; 7z x archive_2.7z -o/{folder_ex}", 'Everything is Ok'), print('test4 FAIL')



# тестирование  просмотра  архива
def test_step_5():
    assert checkout(f"7z l {folder_out}/archive_2.7z", "Scanning the drive for archives"), print("test5 FAIL")



# тест команды crc32 расчета хеша файла
def test_step_6():
    assert checkout(f"cd {home}/PycharmProjects/pythonProject; crc32 crc_test.txt", crc('crc_test.txt')), print("test6 FAIL")

if __name__ == '__main__':
    pytest.main(['-vv'])
