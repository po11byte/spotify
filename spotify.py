import streamlit as st
import requests
import base64

st.set_page_config(page_title="Music Explorer App", layout="centered")

st.title("Music Explorer")
st.write("Busca canciones, artistas o álbumes desde Spotify.")

CLIENT_ID = "1aefb8a907db6f0953a604ab4d387020"
CLIENT_SECRET = "1aefb8a907db6f0953a604ab4d387020"

def get_spotify_token():
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {auth_base64}"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

def search_music(query, token):
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=5"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

busqueda = st.text_input("Escribe el nombre de una canción o artista:")

if st.button("Buscar Música"):
    if not CLIENT_ID or not CLIENT_SECRET:
        st.error("Por favor configura tus credenciales de Spotify")
    elif busqueda:
        token = get_spotify_token()
        resultados = search_music(busqueda, token)
        if "tracks" in resultados and resultados["tracks"]["items"]:
            st.success("Resultados encontrados:")
            for track in resultados["tracks"]["items"]:
                st.subheader(track["name"])
                st.write(f"Artista: {track['artists'][0]['name']}")
                st.write(f"Álbum: {track['album']['name']}")
                st.image(track["album"]["images"][0]["url"], width=150)
                if track["preview_url"]:
                    st.audio(track["preview_url"], format="audio/mp3")
                st.markdown("---")
        else:
            st.warning("No se encontraron resultados para tu búsqueda.")
    else:
        st.warning("Por favor, escribe algo para buscar.")

st.markdown("---")
st.caption("Desarrollado con Streamlit y Spotify API")