from math import radians, cos, sin, asin, sqrt
import math
import jdatetime
import datetime
from PIL import Image
import numpy as np
import requests
import os
from io import BytesIO

def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
     
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
      
    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000    # Radius of earth in meters

    distance = c * r     #distance in meters
    
    return distance


def bbox_geometry_calculator(bbox):
    #get coords of all four points of the bbox, width, height and area of the bbox
    lon1, lat1, lon2, lat2 = bbox
    
    # point_sw = (lon1, lat1)
    # point_ne =(lon2, lat2)
    # point_nw = (lon1, lat2)
    # point_se = (lon2, lat1)
    
    width =  haversine_distance(lon1, lat1, lon2, lat1)
    height = haversine_distance(lon1, lat1, lon1, lat2)
    area = width * height
    
    return width, height, area



def shamsi_date_time():
    # Get the current Gregorian date and time
    today = jdatetime.date.today()
    day, month, year = today.day, today.month, today.year
    clock = datetime.datetime.now().strftime("%H;%M")

    # Format the Jalali date and time
    formated_datetime = f"{year}_{month}_{day}-{clock}"

    return formated_datetime


def is_image(var):
    return (type(var) == np.ndarray) or (isinstance(var, Image.Image))
    

def verify_coords(coords, inference_mode):
    try:
        lon1, lat1, lon2, lat2 = coords
    except:
        if inference_mode in ["images_dict", "directory"]:
            raise ValueError(f"""bbox_coord_wgs84 should be a python dictionary containing keys equal to the images name and values equals to wgs84 coordinations in a list which is as follows:\n[West Longitude , South Latitude , East Longitude , North Latitude]""")
        else:
            raise ValueError(f"""bbox_coord_wgs84 can be a list, a tuple or a dictionary a key (anything) and value equals to wgs84 coordinations in a list or tuple rtpe which is as follows:\n[West Longitude , South Latitude , East Longitude , North Latitude]""")
    if (lon1 > lon2) or (lat1 > lat2):
        raise ValueError("""bbox_coord_wgs84 is supposed to be in the following format:\n[left, bottom, right, top]\nor in other words:\n[min Longitude , min Latitude , max Longitude , max Latitude]\nor in other words:\n[West Longitude , South Latitude , East Longitude , North Latitude]""")
    if any([(lon1 > 180), (lon2 > 180),
            (lon1 < -180), (lon2 < -180),
            (lat1 > 90), (lat2 > 90),
            (lat1 < -90), (lat2 < -90)]):
        raise ValueError("""Wrong coordinations! Latitude is between -90 and 90 and Longitude is between -180 and 180. Also, the following format is required:\n[left, bottom, right, top]\nor in other words:\n[min Longitude , min Latitude , max Longitude , max Latitude]\nor in other words:\n[West Longitude , South Latitude , East Longitude , North Latitude]""")
    coords_verified = True
    return coords_verified, lon1, lat1, lon2, lat2


def calculate_scale_down_factor(area, model_input_dim=768, a=0.2 , b=0.75, threshold=1.5):
    average_dim =  math.sqrt(area)
    dim_ratio = average_dim / model_input_dim
    if dim_ratio > threshold:
        scale_factor = (a * dim_ratio) + b
    else:
        scale_factor = 1
    scale_factor = max(scale_factor, 1)
    return scale_factor


def bbox_divide(bbox, lon_step=0.05, lat_step=0.05):
    m = str(lon_step)[::-1].find('.')
    lon1_ref, lat1_ref, lon2_ref, lat2_ref = bbox
    h_bbox = lat2_ref - lat1_ref
    w_bbox = lon2_ref - lon1_ref
    lon_no_steps = int(w_bbox//lon_step) + 1
    lat_no_steps = int(h_bbox//lat_step) + 1
    bboxes = []
    for h_partition in range(lat_no_steps):
        lat1 = lat1_ref + h_partition * lat_step
        lat2 = lat1 + lat_step
        lat1, lat2 = map(lambda x: round(x, m), [lat1, lat2])
        bboxes_row = []
        for w_partition in range(lon_no_steps):
            lon1 = lon1_ref + w_partition * lon_step
            lon2 = lon1 + lon_step
            lon1, lon2 = map(lambda x: round(x, m), [lon1, lon2])
            bboxes_row.append([lon1, lat1, lon2, lat2])
        bboxes.append(bboxes_row)
    return bboxes


def xyz2bbox(xyz_coords):
    x, y, z = xyz_coords
    lonmin = x / math.pow(2.0, z) * 360.0 - 180
    lonmax = (x+1) / math.pow(2.0, z) * 360.0 - 180
    n1 = math.pi - (2.0 * math.pi * y) / math.pow(2.0, z)
    latmax = math.atan(math.sinh(n1)) * 180 / math.pi
    n2 = math.pi - (2.0 * math.pi * (y+1)) / math.pow(2.0, z)
    latmin = math.atan(math.sinh(n2)) * 180 / math.pi
    coords = (lonmin, latmin, lonmax, latmax)
    return coords


def bbox2xyz(bbox_coords):
    lonmin, latmin, lonmax, latmax = bbox_coords
    z = math.log(360.0 / (lonmax - lonmin), 2.0)
    x = math.pow(2.0, z) * (lonmin + 180) / 360
    a = math.tan(math.pi * latmax / 180)
    y = (math.pi - math.log(a + math.sqrt(a**2 + 1), math.e)) * math.pow(2.0, z) / (2*math.pi)
    return x, y, int(z)


def xyz2bbox_territory(x_range, y_range, zoom):
    lonmin, _, _, latmax = xyz2bbox((x_range[0], y_range[0], zoom))
    _, latmin, lonmax, _ = xyz2bbox((x_range[1], y_range[1], zoom))
    coords = (lonmin, latmin, lonmax, latmax)
    return coords


def start_end_time_interpreter(start=None, end=None, n_days_before_base_date=None, base_date=None, return_formatted_only=True):
    if n_days_before_base_date != None:
        try:
            n_days_before_base_date = int(n_days_before_base_date)
        except:
            raise ValueError("n_days_before_base_date must be an integer or None.")
        if base_date == None:
            end = datetime.datetime.now()
            start = end - datetime.timedelta(days=n_days_before_base_date)
        elif type(base_date) in [datetime.datetime, datetime.date]:
            end = base_date
            start = end - datetime.timedelta(days=n_days_before_base_date)
        else:
            try:
                end_year, end_month, end_day = map(int, end.split('/'))
            except:
                end_year, end_month, end_day = map(int, end.split('-'))
            end = datetime.date(end_year, end_month, end_day)
            start = end - datetime.timedelta(days=n_days_before_base_date)

    if type(start) not in [datetime.datetime, datetime.date]:
        try:
            start_year, start_month, start_day = map(int, start.split('/'))
        except:
            start_year, start_month, start_day = map(int, start.split('-'))
        start = datetime.date(int(start_year), int(start_month), int(start_day))
    
    if type(end) not in [datetime.datetime, datetime.date]:
        try:
            end_year, end_month, end_day = map(int, end.split('/'))
        except:
            end_year, end_month, end_day = map(int, end.split('-'))
        end = datetime.date(int(end_year), int(end_month), int(end_day))
    # if type(end) not in [datetime.datetime, datetime.date]:
    #     end = base_date
    #     start = end - datetime.timedelta(days=n_days_before_base_date)

    start_formatted = datetime.datetime.strftime(start, "%Y-%m-%dT%H:%M:%SZ")
    end_formatted = datetime.datetime.strftime(end, "%Y-%m-%dT%H:%M:%SZ")
    timestamp = f"{start_formatted.split('T')[0]}_{end_formatted.split('T')[0]}"
    
    if return_formatted_only:
        return [start_formatted, end_formatted, timestamp]
    return [(start, start_formatted), (end, end_formatted), timestamp]



def territory_divider(x_range, y_range, piece_size=70):
    x_min_ref , x_max_ref, y_min_ref, y_max_ref = min(x_range), max(x_range), min(y_range), max(y_range)
    x_length = x_max_ref - x_min_ref
    y_length = y_max_ref - y_min_ref

    x_remainder, y_remainder, x_pieces_opt, y_pieces_opt = piece_size, piece_size, piece_size, piece_size
    piece_size_probable_range= range(int(0.7 * piece_size), int(1.3 * piece_size + 1))
    for i in piece_size_probable_range:
        if (x_length % i) < x_remainder:
            x_remainder = x_length % i
            x_pieces_opt = i
        if (y_length % i) < y_remainder:
            y_remainder = y_length % i
            y_pieces_opt = i

    x_no_steps = max(int(x_length//x_pieces_opt), 1)
    y_no_steps = max(int(y_length//y_pieces_opt), 1)
    territories = []
    for h_partition in range(y_no_steps):
        y_min = y_min_ref + h_partition * y_pieces_opt
        y_max = y_max_ref if (h_partition == y_no_steps - 1) else (y_min + y_pieces_opt)
        territories_row = []
        for w_partition in range(x_no_steps):
            x_min = x_min_ref + w_partition * x_pieces_opt
            x_max = x_max_ref if (w_partition == x_no_steps - 1) else (x_min + x_pieces_opt)
            territories_row.append([(x_min, x_max) , (y_min, y_max)])
        territories.append(territories_row)
    return territories


def coords_in_a_xyz(lon_lat, xyz):
    lon, lat = lon_lat
    x, y, z = xyz
    lonmin, latmin, lonmax, latmax = xyz2bbox(xyz)
    if (lon >= lonmin) and (lon <= lonmax) and (lat >= latmin) and (lat <= latmax):
        return True
    return False


def image_dir_in_image_db(x, y, z, timestamp, base_dir, annotation_mode=False):
    path_z = os.path.join(base_dir, str(int(z)))
    path_zx = os.path.join(path_z, str(int(x)))
    path_zxy = os.path.join(path_zx, str(int(y)))
    if annotation_mode:
        image_path = os.path.join(path_zxy, f"{timestamp}_annot.png")
    else:
        image_path = os.path.join(path_zxy, f"{timestamp}.png")
    return image_path