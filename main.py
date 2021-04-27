from datetime import datetime
from vac import scheduler
import vac

def print_ts(*args, **kwargs):
    ts = datetime.now().strftime('%d/%m/%y-%H:%M:%S - ')
    print(ts, *args, **kwargs)

print_ts('Iniciando consulta')

try:
    vac_scheduler = scheduler.Scheduler(True)

    vac_scheduler.screen_login('vac_user', 'vac_password')

    vac_scheduler.screen_main()

    vac_scheduler.screen_scheduler_appointment(vac_scheduler.locations['SPO'], 1)

    vac_scheduler.screen_applicant_list()

    vac_scheduler.screen_add_applicant('1982-05-01')

    vac_scheduler.wait(15)

    vac_scheduler.logout()

except Exception as e:
    print_ts(str(e))

print_ts('Consulta finalizada')