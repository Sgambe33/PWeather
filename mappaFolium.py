import folium
import iso3166
import pycountry
import geopy
import geojson
from geopy.geocoders import Nominatim
from meteostat import Stations
from folium_jsbutton import JsButton
countryList = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Vatican City', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon',
               'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
geolocator = Nominatim(user_agent="dwerdsfdfs<fs")


def creaMappa():
    m = folium.Map(location=[43.7698712, 11.2555757],
                   prefer_canvas=True, tiles='Stamen Terrain')
    tooltip = "Click me!"
    print(len(countryList))
    f = open("MyFile.txt", "r")
    for x in range(0, 244):
        nomePaese = f.readline()
        lat = f.readline()
        long = f.readline()
        try:
            folium.Marker([float(lat), float(long)], popup="<i>" +
                          nomePaese+"</i>", tooltip=tooltip).add_to(m)
        except:
            Exception
    JsButton(
        title='<i class="fas fa-crosshairs"></i>', function="""
    function(btn, map) {
        map.setView([42.3748204, -71.1161913],5);
        btn.state('zoom-to-forest');
    }
    """).add_to(m)

    # Aggiungo i layer
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Esri Satellite', overlay=True, control=True).add_to(m)
    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('stamenterrain').add_to(m)
    folium.TileLayer('stamentoner').add_to(m)
    folium.TileLayer('stamenwatercolor').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.LayerControl().add_to(m)
    m.save("index.html")


def coordToFile(x, test):
    f = open("MyFile.txt", "a")
    f.write(countryList[x]+"\n")
    f.write(str(test.latitude)+"\n")
    f.write(str(test.longitude)+"\n")
    f.close()


# Get nearby weather stations
stazioni = []
stations = Stations()
stations = stations.region("US", "TX")
nStazioni = stations.count()

stazioni = stations.fetch(nStazioni)
# idEstratti=stazioni.columns
'''print("Coordinate stazione:")
print(stazioni.latitude.values)'''
latitudiniEstratte = stazioni.latitude.values
longitudiniEstratte = stazioni.longitude.values

regionCode_US = pycountry.subdivisions.get(country_code='CH')
print(regionCode_US)


#italia = pycountry.subdivisions.get(code='IT-'+str(x))

# Print DataFrame
print("Info stazione:")
print(stazioni)


creaMappa()
