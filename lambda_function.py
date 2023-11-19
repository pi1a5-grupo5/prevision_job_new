import sys
import json
from funcao_previsao import PrevJob
from connection import DatabaseConnection

db = DatabaseConnection(
    host="carllet-dev.cygduzvreboa.us-east-2.rds.amazonaws.com",
    database="development",
    user="postgres",
    password="0*6Q8uJxI95OSyc$"
)

def handler(event, context): 
    print(f"teste inicio funcao")
    prev_job = PrevJob()
    prev_job.connection = db.connection 

    ganho_diario = prev_job.calcular_ganho_diario('2c244f97-0446-47f3-bb09-eb918ee84cef')
    prop = prev_job.relac_propriedade('2c244f97-0446-47f3-bb09-eb918ee84cef')
    excl =  prev_job.exclusividade('2c244f97-0446-47f3-bb09-eb918ee84cef')
    qtd_dias = prev_job.qtd_dias_trab('2c244f97-0446-47f3-bb09-eb918ee84cef')

    resultado_previsao = prev_job.previsao_faturamento(excl, prop, qtd_dias, ganho_diario)

    prev_job.close_connection()

    return {
        'statusCode': 200,
        'data': resultado_previsao
    }

   

    
