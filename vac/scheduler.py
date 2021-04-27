import rpa as r
from captcha_solver.solver import captcha_solver

class Scheduler():
    __SCHEDULER_URL = 'https://www.google.com'
    __captcha_solver = captcha_solver()
    __email = ''
    __password = ''
    __debug = False
    locations = {
        'BSB': '50',
        'POA': '82',
        'REC': '72',
        'SPO': '71',
        'RJ': '51'
    }

    def __init__(self, debug=False):
        self.__debug = debug
        self.__initialize()

    def __del__(self):
        self.logout()
        r.close()

    def __log(self, step, msg='Executando...'):
        if self.__debug:
            print('{} - {}'.format(step, msg))

    def __initialize(self):
        r.init(visual_automation = True)
        r.url(self.__SCHEDULER_URL)

    def wait_element_exists(self, element):
        if r.exist(element):
            return True
        return False

    def wait(self, seconds):
        r.wait(seconds)

    def _error_handler(self, step, exception):
        print('{} - {}'.format(step, str(exception)))
        self.logout()
        raise exception

    def __type__if_not_none(self, element, value):
        if not value is None:
            r.type(element, value) 

    def logout(self):
        LOGOUT_BUTTON = '/html/body/div[2]/div[1]/div[1]/span/div/form/a/span'
        self.__log('LOGOUT')
        if r.exist(LOGOUT_BUTTON):
            r.click(LOGOUT_BUTTON)

    def __fill_login_forms(self, email, password, mock=False):
        FIELD_EMAIL = '//*[@id="EmailId"]'
        FIELD_PASSWORD = '//*[@id="Password"]'
        FIELD_CAPTCHA = '//*[@id="CaptchaInputText"]'
        IMAGE_CAPTCHA = 'CaptchaImage'

        r.type(FIELD_EMAIL, '[clear]')
        r.type(FIELD_EMAIL, email)
        r.type(FIELD_PASSWORD, '[clear]')
        r.type(FIELD_PASSWORD, password)
        r.snap(IMAGE_CAPTCHA, 'captcha.png')

        captcha = self.__captcha_solver.solve('captcha.png', mock=mock)
        r.type(FIELD_CAPTCHA, captcha)

    def screen_login(self, email, password):
        try:
            STEP_NAME = 'LOGIN_SCREEN' 
            ERRO_FIELD = '/html/body/div[2]/div[1]/div[4]/div/form/div[1]/ul/li'
            SUBMIT_BUTTON = '/html/body/div[2]/div[1]/div[4]/div/form/div[4]/input'
            SUBMIT_BUTTON_RETRY = '/html/body/div[2]/div[1]/div[4]/div/form/div[5]/input'

            self.__fill_login_forms(email, password)
            r.click(SUBMIT_BUTTON)

            if r.exist(ERRO_FIELD):
                if r.read(ERRO_FIELD) == 'The verification words are incorrect.':
                    self.__log(STEP_NAME, 'Erro no captcha tentando novamente...')
                    self.__fill_login_forms(email, password)
                    r.click(SUBMIT_BUTTON_RETRY)

        except Exception as e:
            self._error_handler('Login screen', e)

    def screen_main(self):
        STEP_NAME = 'MAIN_SCREEN' 
        self.__log(STEP_NAME)
        r.click('/html/body/div[2]/div[1]/div[2]/div/div/div[2]/div/ul/li[1]/a')

    def screen_scheduler_appointment(self, location, nro_applicants):
        try:
            LOCATION_FIELD = '//*[@id="LocationId"]'
            NRO_APPLICATIONS_FIELD = '//*[@id="NoOfApplicantId"]'
            AGREED_FIELD = '//*[@id="IAgree"]'
            CONTINUE_FIELD = '//*[@id="btnContinue"]'
            STEP_NAME = 'SCHEDULER_APPOINTMENT_SCREEN' 
            self.__log(STEP_NAME)

            self.wait_element_exists(CONTINUE_FIELD)
            self.wait(1)

            self.wait_element_exists(LOCATION_FIELD)
            r.select(LOCATION_FIELD, option_value=location)

            self.wait_element_exists(NRO_APPLICATIONS_FIELD)
            r.select(NRO_APPLICATIONS_FIELD, option_value=str(nro_applicants))

            self.wait_element_exists(AGREED_FIELD)
            r.click(AGREED_FIELD)
            r.click(CONTINUE_FIELD)
        except Exception as e:
            self._error_handler('Scheduler Appointment screen', e)

    def screen_applicant_list(self):
        try:
            APPLICANT_BUTTON = '/html/body/div[2]/div[1]/div[3]/div[2]/a'
            STEP_NAME = 'APPLICANT_LIST_SCREEN' 
            self.__log(STEP_NAME)

            self.wait_element_exists(APPLICANT_BUTTON)

            # Add Applicant button
            r.click(APPLICANT_BUTTON)

        except Exception as e:
            self._error_handler('Applicant list screen', e)

    def screen_add_applicant(self, date_of_birth=None, first_name=None, last_name=None, dial_code=None, mobile=None, email_id=None):
        try:
            DATE_OF_BIRTH = '//*[@id="DateOfBirth"]'
            STEP_NAME = 'ADD_APPLICANT_SCREEN' 
            self.__log(STEP_NAME)

            self.wait_element_exists(DATE_OF_BIRTH)

            self.__type__if_not_none(DATE_OF_BIRTH, date_of_birth)
            self.__type__if_not_none('//*[@id="FirstName"]', first_name)
            self.__type__if_not_none('//*[@id="LastName"]', last_name)
            self.__type__if_not_none('//*[@id="DialCode"]', dial_code)
            self.__type__if_not_none('//*[@id="Mobile"]', mobile)
            self.__type__if_not_none('//*[@id="validateEmailId"]', email_id)

            r.click('//*[@id="submitbuttonId"]')

            self.wait(1)
            r.keyboard('[enter]')
        except Exception as e:
            self._error_handler('Add Applicant screen', e)