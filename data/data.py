import mysql.connector
from mysql.connector import errorcode
import json

# connect to mysql
DB_NAME = 'taipeiTrip'
cnx = mysql.connector.connect(user='abc',
                              password='12345678',
                              auth_plugin='mysql_native_password')
cursor = cnx.cursor()

# Create datebase if not exist
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

# Creating table
TABLES = {}
TABLES['attractions'] = (
    "CREATE TABLE `attractions` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `name` VARCHAR(255) NOT NULL,"
    "  `category` VARCHAR(255) NOT NULL,"
    "  `description` TEXT NOT NULL,"
    "  `address` VARCHAR(255) NOT NULL,"
    "  `transport` TEXT NOT NULL,"
    "  `mrt` VARCHAR(255) DEFAULT NULL,"
    "  `latitude` DOUBLE NOT NULL,"
    "  `longtitude` DOUBLE NOT NULL,"
    "  `images` JSON,"
    "  PRIMARY KEY (`id`)"
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


add_attraction = ("INSERT INTO attractions"
                  "(name, category, description, address, transport, mrt, latitude, longtitude, images)"
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ")

# Opening JSON file
f = open('taipei-attractions.json')
 
# returns JSON object as a dictionary
data = json.load(f)
data = data['result']['results']

# save every image url in seperate array

for i in range(len(data)):   
    url = data[i]["file"].split('https:')
    #print(url)
    imageUrls = []
    for j in range(1, len(url)):
        #print(url[j][-3:])
        if url[j][-3:] == "jpg" or url[j][-3:] == "JPG" or url[j][-3:] == "png" or url[j][-3:] == "PNG":
            imageUrl = "https:" +  url[j]
            imageUrls.append(imageUrl)
            #print(imageUrls)
    data_value = (data[i]["stitle"], data[i]["CAT2"],data[i]["xbody"],data[i]["address"],data[i]["info"],data[i]["MRT"],data[i]["latitude"],data[i]["longitude"], json.dumps(imageUrls))
    cursor.execute(add_attraction, data_value)


cnx.commit()

print('closing')
cursor.close()
cnx.close()
