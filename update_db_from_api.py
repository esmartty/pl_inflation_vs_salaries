import value
import polec_db

def update_sourse():

    value_table_dict = {'avg_gross_wages':'avg_total_gross_wages','price_index':'price_indices'}
    #{name of value in var-id table in polec db: name of table in polec db, where these values are writing in}

    for value_name, write_table_name in value_table_dict.items():

        var_id_region_list = polec_db.reading(value_name)

        gross_values = value.get_from_api(var_id_region_list)

        polec_db.writing (gross_values, write_table_name)

update_sourse()
