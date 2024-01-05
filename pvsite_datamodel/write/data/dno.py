""" The script adds the relevant GSP to the sites.

Might need to install nowcasting_dataset

and we want to added the gsp as {gsp_id}|{gsp_nam} into the database

1. Load in dno data from NG
2. Load all sites
3. For each site add dno

"""
import logging
import os
import ssl

import geopandas as gpd
from shapely.geometry import Point

from pvsite_datamodel.write.data.utils import lat_lon_to_osgb

logger = logging.getLogger(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
dno_local_file = f"{dir_path}/dno"


def download_dno():
    """Download DNO data from NG."""

    logger.debug("Getting dno file")
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://data.nationalgrideso.com/backend/dataset/0e377f16-95e9-4c15-a1fc-49e06a39cfa0/resource/e96db306-aaa8-45be-aecd-65b34d38923a/download/dno_license_areas_20200506.geojson"  # noqa
    dno_shapes = gpd.read_file(url)

    logger.debug("Saving dno file")
    dno_shapes.to_file(dno_local_file)


def get_dno(latitude, longitude) -> dict:
    """
    Convert a latitude and longitude and returns the dno.

    :param latitude:
    :param longitude:

    :return: dno is this format {"dno_id": dno_id, "name": dno_name, "long_name": dno_long_name}=
    """

    # load file
    dno = gpd.read_file(dno_local_file)

    # change lat lon to osgb
    x, y = lat_lon_to_osgb(lat=latitude, lon=longitude)
    point = Point(x, y)

    # select dno
    mask = dno.contains(point)
    dno = dno[mask]

    # format dno
    if len(dno) == 1:
        dno = dno.iloc[0]

        dno_id = dno["ID"]
        name = dno["Name"]
        long_name = dno["LongName"]

        dno_dict = {"dno_id": str(dno_id), "name": name, "long_name": long_name}
        logger.debug(dno_dict)
    else:
        dno_dict = {"dno_id": "999", "name": "unknown", "long_name": "unknown"}

    return dno_dict


#
