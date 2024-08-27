# %%
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import pandas as pd
from adjustText import adjust_text
import matplotlib.patheffects as pe


file_dir = os.path.dirname(os.path.realpath(__file__))


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
    os.path.join(file_dir, "country-centroids-override.json")
).set_index("name")
override

# %%
# Override the centroids with custom values
centroids = tradle_countries.copy()
centroids = centroids.combine_first(override)
centroids.update(override)
centroids

# %%
# Plot map with labels
fig, ax = plt.subplots(figsize=(60, 30))
gdf.plot(ax=ax, color="lightblue", edgecolor=(0, 0, 0, 0.2))

texts = []
initial_text_positions = []

for name, data in centroids.iterrows():
    lat = float(data["latitude"])
    lon = float(data["longitude"])
    country_label = label_mapping.get(name, name)
    text = plt.text(
        lon,
        lat,
        country_label,
        fontsize=8,
        ha="center",
        va="center",
        path_effects=[pe.withStroke(linewidth=2, foreground=(1, 1, 1, 0.4))],
    )
    texts.append(text)
    initial_text_positions.append((text.get_position()))
    plt.scatter(lon, lat, color=(1, 0, 0, 0.5), s=5)


# Adjust text positions to avoid overlap
adjust_text(texts, ax=ax, only_move={"text": "xy"})

# Re-check positions and add arrows only if moved significantly
threshold = 2  # Define the significance threshold


# Function to calculate Euclidean distance
def calculate_distance(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


for i, text in enumerate(texts):
    current_position = text.get_position()
    initial_position = initial_text_positions[i]
    distance_moved = calculate_distance(initial_position, current_position)

    if distance_moved > threshold:
        text.set_ha("center")
        text.set_va("center")
        ax.annotate(
            "",
            xy=initial_position,
            xytext=current_position,
            arrowprops=dict(arrowstyle="-", color=(1, 0, 0, 0.5)),
        )

plt.title("Map with Labeled Countries")
plt.tight_layout(pad=0)
plt.savefig("build/map.svg")
plt.savefig("build/map.png")
plt.show()
os.system("open build/map.svg")

# %%
