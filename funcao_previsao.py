import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class PrevJob:
    def calcular_ganho_diario(self, id_condutor):
        cursor = self.connection.cursor()
        sql_query = """
                with tab_aux_perc as (
                select
                    cond_veic.id_condutor,
                    COUNT(DISTINCT TO_CHAR(CAST(perc.data_fim_percurso AS DATE), 'DD-MM-YYYY')) as dt_perc
                from "Condutores_Veiculos" as cond_veic 
				left join "Percurso" as perc on cond_veic."UserVehicleId" = perc."UserVehicleId"
                where cond_veic.id_condutor = %s
				group by 1  
            ),

			tab_aux_ganho as (
                select
                    id_condutor_ganho,
                    sum(valor_ganho) as vlr_ganho
                from "Ganho" as gan	
				group by 1 				
            ),
			
			desv_pd as (
			select id_condutor_ganho,
			case when stddev(vlr_ganho) is null
			then 0
			else stddev(vlr_ganho)
			end as desv_pd
			from tab_aux_ganho
			group by 1
			)
			SELECT
				(tab_aux_ganho.vlr_ganho / NULLIF(tab_aux_perc.dt_perc, 0)) + desv_pd.desv_pd as ganho_diario
			FROM
				tab_aux_ganho
			left join desv_pd on tab_aux_ganho.id_condutor_ganho = desv_pd.id_condutor_ganho
			left join tab_aux_perc on tab_aux_ganho.id_condutor_ganho = tab_aux_perc.id_condutor
			order by 1 asc
			limit 1
        """
        cursor.execute(sql_query, (id_condutor,))
        result = cursor.fetchone()[0]
        return result
    
    def relac_propriedade(self, id_condutor):
        cursor = self.connection.cursor()
        sql_query = """
            with tab_cond_veic as (
                select cond.id, veic.id_veiculo, veic.hodometro, veic.is_alugado
                from usuarios as cond
                left join "Condutores_Veiculos" as cond_veic on cond.id = cond_veic.id_condutor
                left join veiculos as veic on cond_veic.id_veiculo = veic.id_veiculo
                where id_condutor = %s
                ),

                aux_index as (
                select *,
                ROW_NUMBER() OVER (PARTITION BY "id" ORDER BY hodometro desc) AS index
                from tab_cond_veic
                order by "id"
                ),

                carro_mais_km as (
                select 
                    "id",
                    case
                        when index = 1
                    then is_alugado
                    end as prop
                from aux_index
                group by 1,2
				limit 1
                )

                select prop from carro_mais_km
        """
        cursor.execute(sql_query, (id_condutor,))
        result = cursor.fetchone()[0]
        return result
    
    def exclusividade(self, id_condutor):
        cursor = self.connection.cursor()
        sql_query = """
        select 
		case when
		exclusivo is null
		then false
		else exclusivo
		end as exlc
        from usuarios
        where id = %s
        """
        cursor.execute(sql_query, (id_condutor,))
        result = cursor.fetchone()[0]
        return result
    
    def qtd_dias_trab(self, id_condutor):
        cursor = self.connection.cursor()
        sql_query = """
            select 
		case when
		dias_trabalhados is null
		then 22
		else dias_trabalhados
		end as dias_trabalhados
        from usuarios
        where id = %s
        """
        cursor.execute(sql_query, (id_condutor,))
        result = cursor.fetchone()[0]
        return result
    

    def dataset(self):
        cursor = self.connection.cursor()
        sql_query = "SELECT * FROM dataset_view" 
        cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        return df

    def previsao_faturamento(self, excl, prop, qtd_dias_trabalhados, ganho_diario):
        df = self.dataset()
        ganho_diario = float(ganho_diario)
        x = df.drop(['faturamento_liquido', 'id_condutor'], axis=1).values
        y = df['faturamento_liquido'].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)

        md = LinearRegression()
        md.fit(x_train, y_train)
        y_pred = md.predict(x_test)

        vlr_previsto = md.predict([[excl, prop, qtd_dias_trabalhados, ganho_diario]])

        return vlr_previsto[0]