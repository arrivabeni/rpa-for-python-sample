import base64
import requests
import time

class captcha_solver():
    __API_KEY = 'API KEY DO AZCAPTCHA'
    __REQUEST_URL = 'http://azcaptcha.com/in.php?key={}&body={}&method=base64'
    __RESPONSE_URL = 'http://azcaptcha.com/res.php?key={}&id={}&action=get'

    # def __init__(self):

    def __get_request_url(self, img_b64):
        url = self.__REQUEST_URL.format(self.__API_KEY, img_b64)
        return url

    def __get_response_url(self, id):
        url = self.__RESPONSE_URL.format(self.__API_KEY, id)
        return url

    def __image_to_base64(self, file_name):
        with open(file_name, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read())
        return img_b64.decode('utf-8')

    def __send_request(self, img_b64):
        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'} 
            url = self.__get_request_url(img_b64)

            response = requests.post(url, headers=headers) 
            if not str(response.status_code) in '200|202|404':
                raise Exception('HTTP ({})'.format(str(response.status_code)))

            return response.text[3:15]
        except Exception as ex:
            raise Exception('Erro enviando captcha para solver -> {}'.format(ex))

    def __get_response(self, id):
        try:
            url = self.__get_response_url(id)

            response = requests.get(url) 
            if not str(response.status_code) in '200|202|404':
                raise Exception('HTTP ({})'.format(str(response.status_code)))

            return response.text[3:15]
        except Exception as ex:
            raise Exception('Erro recebendo captcha do solver -> {}'.format(ex))

    def solve(self, filename, toUpperCase=True, mock=False):
        if(mock):
            return 'MOCKED'

        img_b64 = self.__image_to_base64(filename)
        id = self.__send_request(img_b64)
        time.sleep(3)

        text = self.__get_response(id)
        return text.upper()
