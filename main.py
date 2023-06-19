import mysql.connector
import config
def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password)
        print("Connection to MySQL database was successful")
    except:
        print("An error has occurred:")
    return connection

connection = create_connection(config.host, config.user, config.password)
