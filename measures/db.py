import sqlite3

conn = sqlite3.connect("measures.sqlite")


def get_areas():
    crs = conn.cursor()
    cmd = "select * from area"
    crs.execute(cmd)

    return crs.fetchall()

def get_area_by_id(requested_id):
    pass