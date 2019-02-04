from views import *

if __name__ == '__main__':
    db.bind('sqlite', 'db.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)

    app.run(debug=True)
