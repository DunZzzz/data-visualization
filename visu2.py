#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 emilien <emilien@emilien-pc>
#

import pandas as pd
import geopandas as gpd
import geoplot as gplt
import matplotlib.pyplot as plt

import mapclassify

def ged171_df():
    return pd.read_csv("./ged171.csv")


def main():
    df = ged171_df()

    world = gpd.read_file(
        gpd.datasets.get_path('naturalearth_lowres')
    )

    # gplt.polyplot(world, figsize=(8, 4))
    print(world['geometry'])
    print(df)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
        df.longitude, df.latitude))
    ax = world.plot(color='white', edgecolor='black')
    gdf.plot(ax=ax, color='red')
    plt.show()

if __name__ == "__main__":
    main()
