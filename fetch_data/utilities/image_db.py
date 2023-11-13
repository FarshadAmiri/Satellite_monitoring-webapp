import os
import cv2
from tqdm import tqdm
import logging
from PIL import Image
import numpy as np
from .sentinel_api import sentinel_query
from .tools import start_end_time_interpreter, xyz2bbox, xyz2bbox_territory, coords_in_a_xyz, image_dir_in_image_db
from .inference_modular import ship_detection
from fetch_data.models import SatteliteImage, DetectedObject, WaterCraft

images_db_path = r"D:\SatteliteImages_db2"

def store_image(x, y, zoom, start=None, end=None, n_days_before_date=None, date=None):
    global image_db_pat
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
    images_meta= []
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
            image_path = image_dir_in_image_db(i, j, zoom, timestamp, base_dir=images_db_path)
            # image_path = os.path.join(path_zxy, f"{timestamp}.png")
            images_meta.append((i, j, image_path))
            if overwrite_repetitious or (os.path.exists(image_path) == False):
                image, url = sentinel_query(coords=(i, j, zoom), start_formatted=start_formatted, end_formatted=end_formatted, output_img=True, output_url=True)
                lonmin, latmin, lonmax, latmax = map(lambda i: round(i,6), xyz2bbox((i, j, zoom)))
                image.save(image_path)
                SatteliteImage.objects.update_or_create(image_path=image_path, x=i, y=j, zoom=zoom, time_from=start_datetime, time_to=end_datetime,
                                                        bbox_lon1=lonmin, bbox_lat1=latmin, bbox_lon2=lonmax, bbox_lat2=latmax, data_source="Sentinel2")
                
                
    if inference:
        logging.info("Inferencing began")
        logging.info("Images concateated for Inferencing")
        concated_img = concatenate_image(x_range, y_range, zoom, start=start, end=end, n_days_before_base_date=n_days_before_base_date, base_date=base_date,
                     images_db_path=images_db_path, return_img=True, save_img=False)
        model_path = r"D:\NLP 1\Sattelite_monitoring-web\fetch_data\utilities\inference_models\best_model.pth"

        coords = xyz2bbox_territory(x_range, y_range, zoom)
        detection_results = ship_detection(concated_img, model_or_model_path=model_path, bbox_coord_wgs84=coords, model_input_dim=768, confidence_threshold=0.9,
                   scale_down_factor=1, sahi_overlap_ratio=0.1, nms_iou_threshold=0.15, device='adaptive', output_dir=None,
                   output_name="prediction", save_annotated_image=False, output_original_image=False, output_annotated_image=True,
                   annotations=["score", "length", "coord"], annotation_font=r"calibri.ttf",annotation_font_size=14, annotation_bbox_width=2)
        ships_data = detection_results["ships_data"]
        annotated_img = detection_results["annotated_image"]

        deconcated_annotated_images = deconcat_image(annotated_img, x_range, y_range)
        for x, y, img in deconcated_annotated_images:
            annot_img_path = image_dir_in_image_db(x, y, zoom, timestamp, base_dir=images_db_path, annotation_mode=True)
            img.save(annot_img_path)
            image_obj = SatteliteImage.objects.get(image_path=image_path)
            image_obj.annotated_image_path = annot_img_path
            image_obj.save()


        for obj, data in ships_data.items():
            for x, y, img_path in images_meta:
                if coords_in_a_xyz(data["lon_lat"], (x, y, zoom)):
                    lon, lat = data["lon_lat"]
                    length = data["length"]
                    confidence = data["confidence"]
                    # watercraft_type = data["watercraft_type"]
                    # watercraft_name = data["watercraft_name"]
                    # awake = data["awake"]
                    # object_type = WaterCraft.objects.get(name=watercraft_name)

                    object_type = WaterCraft.objects.get(name="Unknown")   # !!!!!!!!!!!!!!!!!!!  DEBUG MODE  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    awake = True                                     # !!!!!!!!!!!!!!!!!!!  DEBUG MODE  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                    pk = f"x{x}_y{y}_z{zoom}_({timestamp})_{obj}"
                    image_path = image_dir_in_image_db(x, y, zoom, timestamp, base_dir=images_db_path)
                    source_img = SatteliteImage.objects.get(image_path=img_path)
                    DetectedObject.objects.update_or_create(pk=pk, image=source_img, x=x, y=y, zoom=zoom, lon=lon, lat=lat, time_from=start_datetime,
                                                            time_to=end_datetime, confidence=confidence, length=length, object_type=object_type,
                                                            awake=True)



def concatenate_image(x_range, y_range, zoom, start=None, end=None, n_days_before_base_date=None, base_date=None, images_db_path=images_db_path,
                 return_img=True, save_img=False, save_img_path=r"D:\SatteliteImages_db_concat"):
    _ , _ , timestamp = start_end_time_interpreter(start=start, end=end, n_days_before_base_date=n_days_before_base_date, base_date=base_date,
                                                   return_formatted_only=False)
    path_z = os.path.join(images_db_path, str(int(zoom)))
    images_horizontally = []
    for j in range(y_range[0], y_range[1]+1):
        images_row_path = [os.path.join(path_z, str(i), str(j), f"{timestamp}.png") for i in range(x_range[0], x_range[1]+1)]
        images_row = [np.array(Image.open(img_path)) for img_path in images_row_path]
        images_horizontally.append(cv2.hconcat(images_row))
    concated_image = cv2.vconcat(images_horizontally)
    concated_image = Image.fromarray(concated_image.astype('uint8')).convert('RGB')
    logging.info("Images concateated")
    if save_img:
        if save_img_path is None:
            raise ValueError("You must specify save_img_path")
        if os.path.exists(save_img_path) is False:
            os.mkdir(save_img_path)
        concated_img_path = os.path.join(save_img_path, fr"x({x_range[0]}_{x_range[1]})-y({y_range[0]}_{y_range[1]})-z({zoom})-{timestamp}.png")
        concated_image.save(concated_img_path)
    if return_img:
        return concated_image
    

def deconcat_image(concated_image, x_range, y_range):
    concated_image = np.array(concated_image)
    m = y_range[1] - y_range[0] + 1
    n = x_range[1] - x_range[0] + 1
    
    height = concated_image.shape[0] // m
    width = concated_image.shape[1] // n

    small_images = []

    for idy, y in enumerate(range(y_range[0], y_range[1] + 1)):
        # row_images = []

        for idx, x in enumerate(range(x_range[0], x_range[1] + 1)):
            img = concated_image[idy * height: (idy + 1) * height, idx * width: (idx + 1) * width]
            img = Image.fromarray(img.astype('uint8'))
            small_images.append((x, y, img))
            # row_images.append(img)

        # small_images.append(row_images)

    return small_images