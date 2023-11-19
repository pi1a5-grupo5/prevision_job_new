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
    
    eventBody = json.loads(event['body'])

    prev_job = PrevJob()
    prev_job.connection = db.connection 

    ganho_diario = prev_job.calcular_ganho_diario(eventBody['userId'])
    prop = prev_job.relac_propriedade(eventBody['userId'])
    excl =  prev_job.exclusividade(eventBody['userId'])
    qtd_dias = prev_job.qtd_dias_trab(eventBody['userId'])

    resultado_previsao = prev_job.previsao_faturamento(excl, prop, qtd_dias, ganho_diario)

    prev_job.close_connection()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Previsão de faturamento",
            "resultado_previsao": resultado_previsao
        }),
    }

   

    
