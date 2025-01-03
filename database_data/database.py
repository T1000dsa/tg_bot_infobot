from mysql.connector import connect, Error
from config_data.config import Config, load_config

data:Config = load_config()
data = data.db
def do_save(some_data:dict):
    try:
        connection = connect(
                host = data.db_host,
                user = data.db_user,
                password = data.db_password, 
                database = data.database,
                auth_plugin='mysql_native_password')
        cursor = connection.cursor()
            
        seg_params = [some_data['user_id'],some_data['user_name'], 
                        some_data['is_bot'], some_data['status'],
                        some_data['language']]
            
        create_table_quary = f"""
                        CREATE TABLE IF NOT EXISTS {data.database_table} (
                        id INT AUTO_INCREMENT,
                        user_id BIGINT,
                        user_name TEXT,
                        is_bot TEXT,
                        status TEXT,
                        language TEXT,
                        PRIMARY KEY (id)
                        ); ENGINE = InnoDB
                        """
                    
        cursor.execute(create_table_quary, multi=True)
        connection.commit()
        
        insert_db_query = f'''
            INSERT INTO {data.database_table}
            (user_id, user_name,
            is_bot,status,
            language)
            VALUES (%s, %s, %s, %s, %s)
            '''
        cursor.execute(insert_db_query,
                        seg_params)
        connection.commit()
        cursor.execute(seg_params)
        print('Data insertation was complete')
        
    except(Error) as ee:
        print('Some failure here', ee)
        if ee.args[-1] == '42000':
            connection = connect(
                    host = data.db_host,
                    user = data.db_user,
                    password = data.db_password, 
                    database = data.database,
                    auth_plugin='mysql_native_password')
            
            cursor = connection.cursor()
            create_db_quary = f'CREATE DATABASE IF NOT EXISTS {data.database}'
            cursor.execute(create_db_quary)
            
        print('Creation of table')
        if ee.args[-1] == '42S02':
            connection = connect(
                    host = data.db_host,
                    user = data.db_user,
                    password = data.db_password, 
                    database = data.database,
                    auth_plugin='mysql_native_password')
            
            cursor = connection.cursor()
            create_table_quary = f"""
                    CREATE TABLE {data.database_table} (
                    id INT AUTO_INCREMENT,
                    user_id BIGINT,
                    user_name TEXT,
                    is_bot TEXT,
                    status TEXT,
                    language TEXT,
                    PRIMARY KEY (id)
                    ); ENGINE = InnoDB
                    """
            cursor.execute(create_table_quary)
            connection.commit()


def show_it():
    try:
        connection = connect(
                host = data.db_host,
                user = data.db_user,
                password = data.db_password, 
                database = data.database,
                auth_plugin='mysql_native_password')
        
        cursor = connection.cursor()
        #show all tables data
        show_db = f'''SELECT * FROM {data.database_table}'''
        cursor.execute(show_db)
        result = cursor.fetchall()
        return result
    except(Error) as ee:
        print('Some failure here', ee)


"""drop_quary = f'''DROP TABLE {data['table_name']}'''
        cursor.execute(drop_quary)
        connection.commit()
        print('Drop complete')
        #Delete the table in database"""

def check(data_quary:str):
    connection =  connect(
       host = data.db_host,
       user = data.db_user,
       password = data.db_password, 
       database = data.database,
       auth_plugin='mysql_native_password')
    cursor = connection.cursor()
    cursor.execute(data_quary)
    result = cursor.fetchall()
    return bool(result[0][0])