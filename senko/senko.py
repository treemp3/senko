import urequests, uhashlib, sys


class Senko:
    """原程序基于github代码存储库实现，https请求时内存溢出，修改为http文件服务实现"""

    def __init__(self, url, files=["boot.py", "main.py"], headers={}):
        """Senko OTA agent class.
        Args:
            url (str): URL to root directory.
            files (list): Files included in OTA update.
            headers (list, optional): Headers for urequests.
        """
        self.url = url
        self.headers = headers
        self.files = files

    def _check_hash(self, x, y):
        """检查文件指纹是否一致"""
        x_hash = uhashlib.sha1(x.encode())
        y_hash = uhashlib.sha1(y.encode())

        x = x_hash.digest()
        y = y_hash.digest()

        if str(x) == str(y):
            return True
        else:
            return False

    def _get_file(self, url):
        text = ""
        try:
            payload = urequests.get(url, headers=self.headers)
            code = payload.status_code
            if code == 200:
                text = payload.text
        except OSError as err:
            sys.print_exception(err)
        except Exception as err:
            sys.print_exception(err)

        return text

    def update(self):
        """Replace all changed files with newer one.
        Returns:
            True - if changes were made, False - if not.
        """
        is_changed = False

        for file in self.files:
            print('Now start comparing file differences: {}'.format(file))
            latest_version = self._get_file(self.url + file)
            if not latest_version:
                print('An exception occurred while downloading the latest file')
                break

            try:
                with open(file, "r") as local_file:
                    local_version = local_file.read()
            except:
                print('An exception occurred while reading the local file')
                local_version = ""

            if self._check_hash(latest_version, local_version):
                print('File comparison result: No changed')
                continue

            is_changed = True
            print('The file has changed and a new file will be written')
            with open(file, "w") as local_file:
                local_file.write(latest_version)

        return is_changed
