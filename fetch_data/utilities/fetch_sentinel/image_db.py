import os
from tqdm import tqdm
from .sentinel_api import sentinel_query
from ...models import SatteliteImage

image_db_path = r"D:\SatteliteImages_db"

def store_image(x, y, z, start=None, end=None, n_days_before_date=None, date=None):
    global image_db_path
    image, timestamp = sentinel_query(coords=(x, y, z), start=start, end=end, n_days_before_date=n_days_before_date, date=date, output_img=True, output_timestamp=True)

    if os.path.exists(image_db_path) == False:
        os.mkdir(image_db_path)
    path_z = os.path.join(image_db_path, str(z))
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


def store_image_territory(x_range, y_range, z, start=None, end=None, n_days_before_date=None, date=None, overwrite_repetitious=False, ):
    global image_db_path

    if os.path.exists(image_db_path) == False:
        os.mkdir(image_db_path)
    path_z = os.path.join(image_db_path, str(z))
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
            
            if overwrite_repetitious:
                image, timestamp = sentinel_query(coords=(i, j, z), start=start, end=end, n_days_before_date=n_days_before_date,
                                                  date=date, output_img=True, output_timestamp=True, )
                image_path = os.path.join(path_zxy, f"{timestamp}.png")
                image.save(image_path)
                SatteliteImage.objects.create(image_path=image_path, x=i, y=j, z=z, time_start=timestamp)
            else:
                timestamp = sentinel_query(coords=(i, j, z), start=start, end=end, n_days_before_date=n_days_before_date,
                                                  date=date, output_img=True, output_timestamp=True, return_timestamp_only=True)
                image_path = os.path.join(path_zxy, f"{timestamp}.png")
                if os.path.exists(image_path) == False:
                    image, timestamp = sentinel_query(coords=(i, j, z), start=start, end=end, n_days_before_date=n_days_before_date,
                                                    date=date, output_img=True, output_timestamp=True, )
                    image.save(image_path)
    return f"Done!"