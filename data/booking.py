import mysql.connector
from mysql.connector import errorcode
import json

# connect to mysql
DB_NAME = 'taipeiTrip'
cnx = mysql.connector.connect(user='abc',
                              password='12345678',
                              auth_plugin='mysql_native_password')
cursor = cnx.cursor()

cursor.execute("USE {}".format(DB_NAME))
TABLES = {}
TABLES['booking'] = (
    "CREATE TABLE `booking` ("
    "  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
    "  `user_id` INT NOT NULL,"
    "  `attraction_id` INT NOT NULL,"
    "  `address` VARCHAR(255) NOT NULL,"
    "  `image` VARCHAR(255) NOT NULL,"
    "  `date` VARCHAR(255) NOT NULL,"
    "  `time` VARCHAR(255) NOT NULL,"
    "  `ordertime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "  `price` INT NOT NULL,"
    "   FOREIGN KEY(`user_id`) REFERENCES member (`id`)"
    ") ENGINE=InnoDB")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")