import re

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import rasterstats as rs
import seaborn as sns


def calc_height_stats(plots_path, chm_path, insitu_path, id_colname="Plot_ID"):
    """
    Merge LiDAR and insitu stats into one df
    """

    def calc_lidar_chm_stats(plots_path, chm_path):
        """
        Load lidar CHM centroids and buffer
        """
        plots_gdf = gpd.read_file(plots_path)
        plots_gdf.geometry = plots_gdf.geometry.buffer(distance=20)

        # Get zonal statistics
        chm_stats = rs.zonal_stats(
            plots_gdf,
            chm_path,
            stats=["mean", "max"],
            nodata=0,
            copy_properties=True,
            geojson_out=True)

        chm_stats_gdf = gpd.GeoDataFrame.from_features(chm_stats)
        chm_stats_gdf.rename(columns={"max": "lidar_max",
                                      "mean": "lidar_mean"},
                             inplace=True)

        return (chm_stats_gdf)

    def calc_insitu_height_stats(insitu_path):
        """
        Load insitu data and calculate max and mean
        """
        insitu_df = (
            pd.read_csv(insitu_path)
            .groupby("plotid")
            .stemheight
            .agg(["max", "mean"])
            .rename(columns={"max": "insitu_max", "mean": "insitu_mean"})
        )

        return (insitu_df)

    # Load centroids and buffer
    chm_stats_gdf = calc_lidar_chm_stats(plots_path,
                                         chm_path)

    # Load insitu data and get max, mean
    insitu_df = calc_insitu_height_stats(insitu_path)

    # Make IDs match
    chm_stats_gdf[id_colname] = [
        re.sub("[^0-9]", "", id) for id in chm_stats_gdf[id_colname]]
    insitu_df.index = [re.sub("[^0-9]", "", id) for id in insitu_df.index]

    # Merge dfs
    stats_df = chm_stats_gdf.merge(insitu_df,
                                   right_index=True,
                                   left_on=id_colname)

    return (stats_df)


def plot_max_mean_height(stats_df, mean_axis_max, max_axis_max, site_name):
    """
    Plot the max and mean data for one site
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 12))

    ax1.set(xlim=(0, mean_axis_max), ylim=(0, mean_axis_max), aspect="equal",
            title=site_name + " - Mean Canopy Height")
    ax1.scatter(x=stats_df.lidar_mean, y=stats_df.insitu_mean)
    ax1.plot((0, 1), (0, 1), transform=ax1.transAxes, ls='--', c='k')
    sns.regplot(x="lidar_mean", y="insitu_mean",
                data=stats_df,
                color="purple",
                ax=ax1)

    ax2.set(xlim=(0, max_axis_max), ylim=(0, max_axis_max), aspect="equal",
            title=site_name + " - Max Canopy Height")
    ax2.scatter(x=stats_df.lidar_max, y=stats_df.insitu_max)
    ax2.plot((0, 1), (0, 1), transform=ax2.transAxes, ls='--', c='k')
    sns.regplot(x="lidar_max", y="insitu_max",
                data=stats_df,
                color="purple",
                ax=ax2)
