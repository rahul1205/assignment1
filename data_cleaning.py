def create_app_app_id_dict():
    """
    Utility function to create a dict for app and app_id
    """
    clean_googleplaystore = open("D:\\assignment1\\clean_googleplaystore.csv", 'r', encoding='utf-8')
    app_records = clean_googleplaystore.readlines()
    app_dict = {}
    for a in app_records[1:]:
        app_dict[a.split(',')[1]] = a.split(',')[0]

    return app_dict


def create_genre_dict():

    """
    Utility function to create a dictionary of genres and genre_id
    """
    genres = open("D:\\assignment1\\genre_master.csv", 'r', encoding='utf-8')
    records = genres.readlines()
    genre_dict = {}
    for record in records[1:]:
        genre_dict[record.split(',')[1].strip()] = record.split(',')[0]

    return genre_dict


def remove_duplicates():

    """
    Function to remove duplicate app names and add a primary key to the csv
    """
    f = open("D:\\assignment1\\googleplaystore.csv", 'r', encoding='utf-8')
    records = f.readlines()


    new_f = open("D:\\assignment1\\clean_googleplaystore.csv", 'w+', encoding='utf-8')


    app_name_list = []


    for i, record in enumerate(records):
        # print (record.strip().decode())
        # break
        app_name = record.split(',')[0].strip()
        if not app_name.lower() in app_name_list and not record.split(',')[-1] == '':
            new_f.write(str(i) + ',' +record.replace("\"", ''))
            app_name_list.append(app_name.lower())

    f.close()
    new_f.close()




def create_genre_master():
    """
    Function to create a list for all unique genres
    """
    genre_list = []
    f = open("D:\\assignment1\\app_genre.csv", 'r', encoding='utf-8')
    records = f.readlines()  

    genre_master = open("D:\\assignment1\\genre_master.csv", 'w+', encoding='utf-8')
    heading = 'genre_id,Genres\n'
    genre_master.write(heading)

    for i, record in enumerate(records[1:]):
        if not record.split(',')[-1].strip() in genre_list:
            genre_master.write(str(i) + ',' + record.split(',')[-1])
            # print (record.split(',')[-1])
            genre_list.append(record.split(',')[-1].strip())

    f.close()
    genre_master.close()



def clean_reviews():
    """
    Function to remove nan reviews and add app_id to corresponding apps
    """
    f = open("D:\\assignment1\\googleplaystore_user_reviews.csv", 'r', encoding='utf-8')
    records = f.readlines()

    clean_reviews = open("D:\\assignment1\\clean_googleplaystore_user_reviews.csv", 'w+', encoding='utf-8')

    clean_reviews.write("id,app_id" + ',' + records[0])

    app_dict = create_app_app_id_dict()

    for i, record in enumerate(records[1:]):
        values = record.split(',')
        app_name = record.split(',')[0]
        if not 'nan' in values[1:] and app_name in app_dict.keys():
            try:
                clean_reviews.write(str(i) + ',' + app_dict[app_name] + ',' + record )
            except Exception as e:
                print (str (e), "some exception")

    f.close()
    clean_reviews.close()

def create_app_genre():
    """
    Function to create a csv that will populate app_genre table (temporary, doesn't have genre ID)
    """
    f = open("D:\\assignment1\\clean_googleplaystore.csv", 'r', encoding='utf-8')
    records = f.readlines()    

    genre_dict = create_genre_dict()

    app_genre = open("D:\\assignment1\\app_genre.csv", 'w+', encoding='utf-8')
    heading = 'app_id,genre_id,App,Genres\n'
    app_genre.write(heading)
    # content = []  
    for i, record in enumerate(records[1:]):
        
        genre_list = record.split(',')[-5].split(';')
        # print (i, genre_list)
        for j, genre in enumerate(genre_list):
            try:
                to_write = record.split(',')[0] + ',' + genre_dict[genre.strip()] + ',' + record.split(',')[1] + ',' + genre.strip() + '\n'
            except Exception as e:
                print (str(e) + "some exception occured")
                continue
            # content.append(to_write)
            app_genre.write(to_write)
    f.close()   
    app_genre.close()

# print(create_genre_dict())
# create_app_genre()
# remove_duplicates()
