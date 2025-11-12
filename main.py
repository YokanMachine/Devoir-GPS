import streamlit as st
import folium
from streamlit_folium import st_folium
from PIL import Image, ExifTags
import os
# Récupère les données EXIF d'une image
def get_exif(path):
    ExifData = {}
    try:
        img = Image.open(path)
        infos = img._getexif()
        if infos:
            for tag, value in infos.items():
                Key = ExifTags.TAGS.get(tag, tag)
                if Key == "GPSInfo":
                    gps_data = {}
                    for gps_tag in value:
                        subKey = ExifTags.GPSTAGS.get(gps_tag, gps_tag)
                        gps_data[subKey] = value[gps_tag]
                    ExifData[Key] = gps_data
                else:
                    ExifData[Key] = value
    except Exception as e:
        # Erreur lors de la lecture des données EXIF
        print(f"Erreur lors de la lecture des données EXIF : {e}")
    return ExifData

# Convertit les données GPS EXIF en coordonnées décimales (latitude, longitude)
def gps_etract(exif_data):
    gps_metadata = exif_data['GPSInfo']
    
    lat_ref_num = 1 if gps_metadata['GPSLatitudeRef'] == 'N' else -1

    lat_list = [float(num) for num in gps_metadata['GPSLatitude']]
    lat_coordone = (lat_list[0] + lat_list[1]/60 + lat_list[2]/3600) * lat_ref_num

    long_ref_num = 1 if gps_metadata['GPSLongitudeRef'] == 'E' else -1

    long_list = [float(num) for num in gps_metadata['GPSLongitude']]
    long_coordone = (long_list[0] + long_list[1]/60 + long_list[2]/3600) * long_ref_num

    return (lat_coordone, long_coordone)

# Construire l'app en utulisant STREAMLIT
def Get_Map():
    st.set_page_config(page_title="Visualiseur de photos GPS", layout="wide")
    st.title("Visualiseur de photos")
    st.write("Téléversez des photos et découvrez où elles ont été prises")

    Upleaded_Files = st.file_uploader(label="Donnez vos images", type=["jpg","jpeg","png"], accept_multiple_files=True)

    if Upleaded_Files:
        points = []
        
        for photo in Upleaded_Files:
            # Enregistre temporairement le fichier téléversé
            with open(photo.name, "wb") as p:
                p.write(photo.getbuffer())
            
            # Get EXIF data for this specific photo
            Exif = get_exif(photo.name)
            os.remove(photo.name)
            
            if "GPSInfo" in Exif:
                try:
                    lat, lon = gps_etract(Exif)
                    default_taken = Exif.get("DateTime", "Unknown date")
                    if default_taken != "Unknown date":
                        date_taken = default_taken.split(" ")[0].replace(":", "-")
                    else:
                        date_taken = "Unknown date"
                    points.append({
                        "name": photo.name,
                        "lat": lat,
                        "lon": lon,
                        "date": date_taken
                    })
                except Exception as e:
                    st.warning(f"Impossible d'extraire le GPS de {photo.name} : {e}")
            else:
                st.warning(f"Cette image {photo.name} n'a pas de données GPS.")
                                
        if points:
            if points:
                start_coords = [points[0]["lat"], points[0]["lon"]]
            else:
                start_coords = [48.8566, 2.3522]  
            
            m = folium.Map(location=start_coords, zoom_start=12)
            
            # Des marqueurs pour tous les points
            dates = {}
            for point in points:
                date = point["date"]
                if date not in dates:
                    dates[date] = []
                dates[date].append(point)
                
            # Ajouter des marqueurs et des lignes
            for date,date_points in dates.items():
                # on va dessiner une ligne si tout les poins son dans le meme jour 
                if date_points:
                    date_points.sort(key=lambda p: p["date"])
                    line_coords = [[p["lat"], p["lon"]] for p in date_points]
                    folium.PolyLine(line_coords, color='blue', weight=3).add_to(m)
                    
                for point in date_points:
                    folium.Marker(
                    location=[point["lat"], point["lon"]],
                    tooltip=f"{point['name']}<br>{point['date']}",
                    popup=f"<b>{point['name']}</b><br>Date : {point['date']}",
                    icon=folium.Icon(color="blue", icon="camera"),
                ).add_to(m)
            
            # Display the map
            st_folium(m, width=1200, height=600)
    
Get_Map()