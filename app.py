from flask import Flask
import value
import polec_db

app = Flask(__name__)

@app.route('/')
def from_api_to_db():

    value_table_dict = {'avg_gross_wages':'avg_total_gross_wages','price_index':'price_indices'}
    #{name of value in var-id table in polec db: name of table in polec db, where these values are writing in}

    for value_name, write_table_name in value_table_dict.items():

        var_id_region_list = polec_db.reading(value_name)

        gross_values = value.get_from_api(var_id_region_list)

        polec_db.writing (gross_values, write_table_name)

    return "Done!"

@app.route('/price_indices')
def my_price_api():
    return app.json.response(polec_db.result_values('price_indices'))

@app.route('/avg_total_gross_wages')
def my_avg_gross_wages_api():
    return app.json.response(polec_db.result_values('avg_total_gross_wages'))

if __name__ == "__main__":
    app.run (debug = True)