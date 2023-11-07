import os
from tqdm import tqdm
from .utility_sentinel_api import sentinel_query
from .utility_tools import start_end_time_interpreter, xyz2bbox
from .models import SatteliteImage

# image_db_path = r"D:\SatteliteImages_db"

def store_image(x, y, zoom, start=None, end=None, n_days_before_date=None, date=None):
    global image_db_path
    image, timestamp = sentinel_query(coords=(x, y, zoom), start=start, end=end, n_days_before_date=n_days_before_date, date=date, output_img=True, output_timestamp=True)

    if os.path.exists(image_db_path) == False:
        os.mkdir(image_db_path)
    path_z = os.path.join(image_db_path, str(zoom))
    if os.path.exists(path_z) == False:
        os.mkdir(path_z)
    path_zx = os.path.join(path_z, str(x))
    if os.path.exists(path_zx) == False:
        os.mkdir(path_zx)
    path_zxy = os.path.join(path_zx, str(y))
    if os.path.exists(path_zxy) == False:
        os.mkdir(path_zxy)

    image_path = os.path.join(path_zxy, f"{timestamp}.png")
    image.save(image_path)


def store_image_territory(x_range, y_range, zoom, start=None, end=None, n_days_before_base_date=None, base_date=None,
                          overwrite_repetitious=False, image_store_path="D:\SatteliteImages_db"):

    if os.path.exists(image_store_path) == False:
        os.mkdir(image_store_path)
    path_z = os.path.join(image_store_path, str(zoom))
    if os.path.exists(path_z) == False:
        os.mkdir(path_z)

    for i in tqdm(range(x_range[0], x_range[1]+1)):
        path_zx = os.path.join(path_z, str(i))
        if os.path.exists(path_zx) == False:
            os.mkdir(path_zx)
        for j in tqdm(range(y_range[0], y_range[1]+1)):
            path_zxy = os.path.join(path_zx, str(j))
            if os.path.exists(path_zxy) == False:
                os.mkdir(path_zxy)
            
            start_date, end_date, timestamp = start_end_time_interpreter(start=start, end=end, n_days_before_base_date=n_days_before_base_date,
                                                                base_date=base_date, return_formatted_only=False)
            start_datetime, start_formatted = start_date
            end_datetime, end_formatted = end_date
            image_path = os.path.join(path_zxy, f"{timestamp}.png")

            if overwrite_repetitious or (os.path.exists(image_path) == False):
                image, url = sentinel_query(coords=(i, j, zoom), start_formatted=start_formatted, end_formatted=end_formatted, output_img=True, output_url=True)
                lonmin, latmin, lonmax, latmax = map(lambda i: round(i,6), xyz2bbox((i, j, zoom)))
                image.save(image_path)
                SatteliteImage.objects.update_or_create(image_path=image_path, x=i, y=j, zoom=zoom, time_from=start_datetime, time_to=end_datetime,
                                                        bbox_lon1=lonmin, bbox_lat1=latmin, bbox_lon2=lonmax, bbox_lat2=latmax, data_source="Sentinel2")
    return f"Image saved in the data store and recorded in the database!"