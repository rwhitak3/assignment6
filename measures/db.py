import sqlite3

conn = sqlite3.connect("measures.sqlite")


def get_areas():
    crs = conn.cursor()
    cmd = "select * from area"
    crs.execute(cmd)

    return crs.fetchall()


def get_locations_by_area_id(area_id):
    crs = conn.cursor()
    cmd = "select * from location where location_area = ?"
    crs.execute(cmd, area_id)
    return crs.fetchall()


def get_measures_by_location_id(location_id):
    crs = conn.cursor()
    cmd = "select * from measurements where measurement_location = ?"
    crs.execute(cmd, location_id)
    return crs.fetchall()


def get_categories_by_area_id(area_id):
    crs = conn.cursor()
    cmd = "select category.category_id, category.name, category.description"
    cmd += " from category_area, area , category"
    cmd += " where category_area.category_id = category.category_id"
    cmd += " and category_area.area_id = area.area_id"
    cmd += " and area.area_id = ?"
    crs.execute(cmd, area_id)
    return crs.fetchall()


def get_avg_measurement_by_area_id(area_id):
    crs = conn.cursor()
    cmd = "select avg(measurement.value) from measurement, location "
    cmd +=" where measurement.measurement_location = location.location_id"
    cmd +=" and location_area = ?"
    crs.execute(cmd, area_id)
    return crs.fetchall()

def get_locations_count_by_area_id(area_id):
    crs = conn.cursor()
    cmd = "select count(*) from location where location_area = ?"
    crs.execute(cmd, area_id)
    return crs.fetchall()