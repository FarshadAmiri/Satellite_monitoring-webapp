import os
import cv2
from tqdm import tqdm
import logging
from PIL import Image
import numpy as np
from .sentinel_api import sentinel_query
from .tools import start_end_time_interpreter, xyz2bbox, xyz2bbox_territory
from .inference_modular import ship_detection
from fetch_data.models import SatteliteImage

images_db_path = r"D:\SatteliteImages_db"

def store_image(x, y, zoom, start=None, end=None, n_days_before_date=None, date=None):
    global image_db_path
    image, timestamp = sentinel_query(coords=(x, y, zoom), start=start, end=end, n_days_before_date=n_days_before_date, date=date, output_img=True, output_timestamp=True)

    if os.path.exists(images_db_path) == False:
        os.mkdir(images_db_path)
    path_z = os.path.join(images_db_path, str(zoom))
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


def territory_fetch_inference(x_range, y_range, zoom, start=None, end=None, n_days_before_base_date=None, base_date=None,
                          overwrite_repetitious=False, images_db_path=images_db_path, inference=True):
    
    start_date, end_date, timestamp = start_end_time_interpreter(start=start, end=end, n_days_before_base_date=n_days_before_base_date,
                                                    base_date=base_date, return_formatted_only=False)
    start_datetime, start_formatted = start_date
    end_datetime, end_formatted = end_date
    if os.path.exists(images_db_path) == False:
        os.mkdir(images_db_path)
    path_z = os.path.join(images_db_path, str(zoom))
    if os.path.exists(path_z) == False:
        os.mkdir(path_z)
    img_index = dict()
    for i in tqdm(range(x_range[0], x_range[1]+1)):
        path_zx = os.path.join(path_z, str(i))
        if os.path.exists(path_zx) == False:
            os.mkdir(path_zx)
        for j in tqdm(range(y_range[0], y_range[1]+1)):
            path_zxy = os.path.join(path_zx, str(j))
            if os.path.exists(path_zxy) == False:
                os.mkdir(path_zxy)
            
            # start_datetime, start_formatted = start_date
            # end_datetime, end_formatted = end_date
            image_path = os.path.join(path_zxy, f"{timestamp}.png")
            img_index[f"{i}_{j}"] = image_path
            if overwrite_repetitious or (os.path.exists(image_path) == False):
                image, url = sentinel_query(coords=(i, j, zoom), start_formatted=start_formatted, end_formatted=end_formatted, output_img=True, output_url=True)
                lonmin, latmin, lonmax, latmax = map(lambda i: round(i,6), xyz2bbox((i, j, zoom)))
                image.save(image_path)
                SatteliteImage.objects.update_or_create(image_path=image_path, x=i, y=j, zoom=zoom, time_from=start_datetime, time_to=end_datetime,
                                                        bbox_lon1=lonmin, bbox_lat1=latmin, bbox_lon2=lonmax, bbox_lat2=latmax, data_source="Sentinel2")
                
                
    if inference:
        logging.info("Inferencing began")
        logging.info("Images concateated for Inferencing")
        concat_img = concat_image(x_range, y_range, zoom, start=start, end=end, n_days_before_base_date=n_days_before_base_date, base_date=base_date,
                     images_db_path=r"D:\SatteliteImages_db", return_img=True, save_img=False)
        model_path = r"D:\NLP 1\Sattelite_monitoring-web\fetch_data\utilities\inference_models\best_model.pth"

        coords = xyz2bbox_territory(x_range, y_range, zoom)
        detection_results = ship_detection(concat_img, model_or_model_path=model_path, bbox_coord_wgs84=coords, model_input_dim=768, confidence_threshold=0.9,
                   scale_down_factor=1, sahi_overlap_ratio=0.1, nms_iou_threshold=0.15, device='adaptive', output_dir=None,
                   output_name="prediction", save_annotated_image=False, output_original_image=False, output_annotated_image=True,
                   annotations=["score", "length", "coord"], annotation_font=r"calibri.ttf",annotation_font_size=14, annotation_bbox_width=2)
        annotated_img = detection_results["annotated_image"]
        ships_coords = detection_results["bbox_coords"]
        # ships.lengths ,




def concat_image(x_range, y_range, zoom, start=None, end=None, n_days_before_base_date=None, base_date=None, images_db_path=r"D:\SatteliteImages_db",
                 return_img=True, save_img=False, save_img_path=r"D:\SatteliteImages_db_concat"):
    _ , _ , timestamp = start_end_time_interpreter(start=start, end=end, n_days_before_base_date=n_days_before_base_date, base_date=base_date,
                                                   return_formatted_only=False)
    path_z = os.path.join(images_db_path, str(int(zoom)))
    images_horizontally = []
    for j in range(y_range[0], y_range[1]+1):
        images_row_path = [os.path.join(path_z, str(i), str(j), timestamp) for i in range(x_range[0], x_range[1]+1)]
        images_row = [np.array(Image.open(img_path)) for img_path in images_row_path]
        images_horizontally.append(cv2.hconcat(images_row))
    concat_image = cv2.vconcat(images_horizontally)
    concat_image = Image.fromarray(concat_image.astype('uint8')).convert('RGB')
    logging.info("Images concateated")
    if save_img:
        if save_img_path is None:
            raise ValueError("You must specify save_img_path")
        if os.path.exists(save_img_path) is False:
            os.mkdir(save_img_path)
        concat_img_path = os.path.join(save_img_path, fr"x({x_range[0]}_{x_range[1]})-y({y_range[0]}_{y_range[1]})-z({zoom})-{timestamp}.png")
        concat_image.save(concat_img_path)
    if return_img:
        return concat_image