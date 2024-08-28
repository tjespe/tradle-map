# %%
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from adjustText import adjust_text
import matplotlib.patheffects as pe


file_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(file_dir)


# %%
# List of country names and territories from Tradle
tradle_countries = pd.read_json(
    os.path.join(file_dir, "tradle-countries.json")
).set_index("name")
tradle_countries

# %%
# Load world map
shapefile_dir = "50m_cultural"
shapefile_dir = os.path.join(file_dir, shapefile_dir)
shapefile_paths = [
    "ne_50m_admin_0_countries.shp",
    "ne_50m_admin_0_pacific_groupings.shp",
    "ne_50m_admin_0_sovereignty.shp",
]
gdfs = [gpd.read_file(os.path.join(shapefile_dir, path)) for path in shapefile_paths]
gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
gdf

# %%
# Map some Tradle countries to different labels for aesthetic purposes
label_mapping = {
    "Antigua and Barbuda": "Antigua",
    "Bosnia and Herzegovina": "Bosnia",
    "Saint Kitts and Nevis": "St. Kitts",
    "Saint Barthélemy": "St. Barthelemy",
    "Saint Vincent and the Grenadines": "St. Vincent",
    "Saint Lucia": "St. Lucia",
    "Saint Maarten": "St. Maarten",
    "British Virgin Islands": "Virgin Islands",
    "Democratic Republic of the Congo": "Congo [DRC]",
    "Netherlands Antilles": "Antilles",
    "Congo": "Congo [Republic]",
}
# %%
# Load custom override of centroids
override = pd.read_json(
    os.path.join(file_dir, "text-location-override.json")
).set_index("name")
override

# %%
# Override the centroids with custom values
centroids = tradle_countries.copy()
centroids = centroids.combine_first(override)
centroids.update(override)
centroids["text_latitude"].fillna(centroids["latitude"], inplace=True)
centroids["text_longitude"].fillna(centroids["longitude"], inplace=True)
centroids

# %%
# Plot map with labels
fig, ax = plt.subplots(figsize=(60, 30))
gdf.plot(ax=ax, color="#ffe0b2", edgecolor=(0, 0, 0, 0.2))

# Set blue background
fig.patch.set_facecolor("#b3e5fc")

texts = []

for name, data in centroids.iterrows():
    text_lat = float(data["text_latitude"])
    text_lon = float(data["text_longitude"])
    lat = float(data["latitude"])
    lon = float(data["longitude"])
    country_label = label_mapping.get(name, name)
    text = plt.text(
        text_lon,
        text_lat,
        country_label,
        fontsize=8,
        ha="center",
        va="center",
        path_effects=[pe.withStroke(linewidth=2, foreground=(1, 1, 1, 0.6))],
    )
    if lat == text_lat and lon == text_lon:
        texts.append(text)
    plt.scatter(
        lon,
        lat,
        color=(1, 0, 0, 0.5),
        s=5,
    )


# Adjust text positions to avoid overlap
adjust_text(
    texts,
    ax=ax,
    only_move={"text": "xy"},
    min_arrow_len=0,
    arrowprops=dict(arrowstyle="-", color=(1, 0, 0, 0.4)),
    expand=(1.05, 1.05),
    pull_threshold=5,
)


plt.tight_layout()
ax.set_xlim(-180, 180)
ax.set_ylim(-90, 90)
ax.axis("off")
plt.gca().set_position((0, 0, 1, 1))
plt.savefig("build/map.svg")
plt.savefig("build/map.pdf")
plt.savefig("build/map.png", dpi=300)
plt.show()
os.system("open build/map.svg")
os.system("pdfposter -mA4 -pA0 build/map.pdf build/map-for-print.pdf")

# %%
