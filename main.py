# %%
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import pandas as pd
from adjustText import adjust_text
import matplotlib.patheffects as pe


# %%
# List of country names and territories from Tradle
tradle_countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    "Angola",
    "Anguilla",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bermuda",
    "Bhutan",
    "Bolivia",
    "Bonaire",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "British Virgin Islands",
    "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cape Verde",
    "Cayman Islands",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Christmas Island",
    "Cocos Islands",
    "Colombia",
    "Comoros",
    "Cook Islands",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Curacao",
    "Cyprus",
    "Czechia",
    "Côte d'Ivoire",
    "Democratic Republic of the Congo",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Falkland Islands",
    "Fiji",
    "Finland",
    "France",
    "French Polynesia",
    "French Southern Territories",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jersey",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kosovo",
    "Kuwait",
    "Kyrgyzstan",
    "Laos",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Lithuania",
    "Luxembourg",
    "Macau",
    "Macedonia",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Martinique",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "Netherlands Antilles",
    "New Caledonia",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "Norfolk Island",
    "North Korea",
    "Northern Mariana Islands",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Pitcairn Islands",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Republic of the Congo",
    "Romania",
    "Russia",
    "Rwanda",
    "Saint Barthelemy",
    "Saint Helena",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Maarten",
    "Saint Pierre and Miquelon",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Korea",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syria",
    "São Tomé and Príncipe",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tokelau",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Turks and Caicos Islands",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela",
    "Vietnam",
    "Wallis and Futuna",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]

# %%
# Load world map
shapefile_dir = "50m_cultural"
file_dir = os.path.dirname(os.path.realpath(__file__))
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
# Load ISO 3166-1 country centroids
iso_centroids = pd.read_json(
    os.path.join(file_dir, "iso-country-centroids.json")
).set_index("name")
iso_centroids

# %%
# Load custom override of centroids
override = pd.read_json(
    os.path.join(file_dir, "country-centroids-override.json")
).set_index("name")
override

# %%
# Override the centroids with custom values
centroids = iso_centroids.copy()
centroids = centroids.combine_first(override)
centroids.update(override)
centroids

# %%
# Map Tradle country names to ISO names
iso_mapping = {
    "Democratic Republic of the Congo": "Congo [DRC]",
    "Ivory Coast": "Côte d'Ivoire",
    "Myanmar": "Myanmar [Burma]",
    "Republic of the Congo": "Congo [Republic]",
    "United States of America": "United States",
    "Falkland Islands": "Falkland Islands [Islas Malvinas]",
    "Palestine": "Gaza Strip",  # Assuming Palestine refers to the Gaza Strip
    "Eswatini": "Swaziland",
    "Cocos Islands": "Cocos [Keeling] Islands",
    "Czechia": "Czech Republic",
    "Macedonia": "Macedonia [FYROM]",
    "Saint Maarten": "Saint Martin",
}
mapped_countries = set(
    iso_mapping.get(country, country) for country in tradle_countries
)

# %%
# Check if all countries were found
found_countries = set(centroids.index.unique())
missing_countries = mapped_countries - found_countries
if missing_countries:
    print(
        f"Could not find the following {len(missing_countries)} countries: {missing_countries}"
    )
    not_used = found_countries - mapped_countries
    print(
        f"The following {len(not_used)} countries exist in ISO but was not used: {not_used}"
    )

# %%
# Map some Tradle countries to different labels for aesthetic purposes
label_mapping = {
    "Antigua and Barbuda": "Antigua",
    "Bosnia and Herzegovina": "Bosnia",
    "Saint Kitts and Nevis": "St. Kitts",
    "Saint Barthelemy": "St. Barthelemy",
    "Saint Vincent and the Grenadines": "St. Vincent",
    "Saint Lucia": "St. Lucia",
    "Saint Maarten": "St. Maarten",
    "British Virgin Islands": "Virgin Islands",
    "Democratic Republic of the Congo": "Congo [DRC]",
}

# %%
# Plot map with labels
fig, ax = plt.subplots(figsize=(60, 30))
gdf.plot(ax=ax, color="lightblue", edgecolor=(0, 0, 0, 0.2))

texts = []
initial_text_positions = []

for tradle_country in tradle_countries:
    iso_country = iso_mapping.get(tradle_country, tradle_country)
    try:
        row = centroids.loc[iso_country]
    except KeyError as e:
        print(f"Could not find {iso_country}")
        continue
    lat = float(row["latitude"])
    lon = float(row["longitude"])
    country_label = label_mapping.get(tradle_country, tradle_country)
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
