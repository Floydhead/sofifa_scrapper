import db
import pandas as pd
import helpers as h

#conn = db.connect_db('tidb').connect()
#print(conn, type(conn))
my_data = h.read_db(schema='ocm', table='playerids')
#my_data = pd.read_sql_table(schema='ocm', table_name='playerids',con=conn)
print(my_data)