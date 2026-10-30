
from flask import Flask, request, render_template
import xml.etree.ElementTree as ET

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    input_gpx = ""
    output_gpx = ""
    error = ""

    if request.method == "POST":
        input_gpx = request.form.get("gpx_content", "")

        if not input_gpx.strip():
            error = "Please enter GPX content."

        else:
            try:
                root = ET.fromstring(input_gpx)

                new_root = ET.Element("gpx", {
                    "version": "1.1",
                    "Visit": "https://discord.gg/iPogo"
                })

                count = 0

                for point in root.findall(".//{*}trkpt"):
                    lat = point.get("lat")
                    lon = point.get("lon")

                    if lat is not None and lon is not None:
                        ET.SubElement(new_root, "wpt", {
                            "lat": lat,
                            "lon": lon
                        })
                        count += 1

                if count == 0:
                    error = "No track points were found in this GPX content."

                else:
                    lines = [
                        '<?xml version="1.0" encoding="utf-8" standalone="yes"?>',
                        '<gpx version="1.1" Visit="https://discord.gg/iPogo">'
                    ]

                    for waypoint in new_root.findall("wpt"):
                        lat = waypoint.get("lat")
                        lon = waypoint.get("lon")

                        lines.append(
                            f'<wpt lat="{lat}" lon="{lon}"></wpt>'
                        )

                    lines.append('</gpx>')

                    output_gpx = "\n".join(lines)


            except ET.ParseError:
                error = "The entered content is not valid XML."

    return render_template(
        "index.html",
        input_gpx=input_gpx,
        output_gpx=output_gpx,
        error=error
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
