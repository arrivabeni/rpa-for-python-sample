import rpa as r
from captcha_solver.solver import captcha_solver
from datetime import datetime

def print_ts(*args, **kwargs):
    ts = datetime.now().strftime('%d/%m/%y-%H:%M:%S - ')
    print(ts, *args, **kwargs)

print_ts('Iniciando consulta')

# - Inicializa browser
r.init()
r.url('https://cv.numenit.com.br/teste.html')



# <option value="50">Canada Visa Application Center - Brasilia</option>
# <option value="82">Canada Visa Application Center - Porto Alegre</option>
# <option value="72">Canada Visa Application Center - Recife - PE</option>
# <option value="71">Canada Visa Application Center - Sao Paulo</option>
# <option value="51">Canada Visa Application Center - Rio de Janeiro</option>
r.select('//*[@id="LocationId"]', option_value='71')


r.wait(10)





print_ts('Consulta finalizada')