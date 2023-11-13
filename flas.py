from flask import Flask,render_template, request,jsonify,render_template_string
from streamlit_folium import st_folium
import streamlit as st
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

app = Flask(__name__,template_folder="public") 

import folium


app = Flask(__name__)



@app.route('/')
def home():
    return "welcome to flask form streamlit"
def main():
    """Simple example of a fullscreen map."""
    m = folium.Map()
    folium.LatLngPopup().add_to(m)

    return st.write(m._repr_html_(), unsafe_allow_html=True)


@app.route("/react",methods = ['POST'])
def react():
    data = request.get_json()
    result = "AKN"
    return jsonify(result=result)




@app.route("/iframe")
def iframe():
    """Embed a map as an iframe on a page."""
    m = folium.Map()

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>Using an iframe</h1>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )


@app.route("/components")
def components():
    """Extract map components and put those on a page."""
    m = folium.Map(
        width=800,
        height=600,
    )

    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head>
                    {{ header|safe }}
                </head>
                <body>
                    <h1>Using components</h1>
                    {{ body_html|safe }}
                    <script>
                        {{ script|safe }}
                    </script>
                </body>
            </html>
        """,
        header=header,
        body_html=body_html,
        script=script,
    )


if __name__ == "__main__":
    app.run(debug=True)