from flask import Flask, request, send_file, jsonify
from bin.filters import apply_filter, apply_custom_filter

app = Flask(__name__)

# Read the PIL document to find out which filters are available out-of the box
filters_available = ["blur" ,
                    "contour" ,
                    "detail" ,
                    "edge_enhance" ,
                    "edge_enhance_more" ,
                    "emboss" ,
                    "find_edges" ,
                    "sharpen" ,
                    "smooth" ,
                    "smooth_more" ,
                    "MYFILTER"
                    ]
custom_filters = ["sepia", "black_and_white", "invert"]



@app.route("/", methods=["GET", "POST"])
def index():
    """
    TODO:
    1. Return the usage instructions that specifies which filters are available, and the method format
    """
    response = {"filters_available": filters_available+custom_filters,
                "usage": {"method": "POST", "url": "/<filter_available>"}
                }
    return jsonify(response)


@app.post("/<filter>")
def image_filter(filter):
    """
    TODO:
    1. Checks if the provided filter is available, if not, return an error
    2. Check if a file has been provided in the POST request, if not return an error
    3. Apply the filter using apply_filter() method from bin.filters
    4. Return the filtered image as response
    """
    pass
    if (filter not in filters_available) and (filter not in custom_filters):
        return jsonify({"error": "Filter not available"})

    file = request.files["image"]
    if not file: 
        return jsonify({"error": "No file provided"})
    if filter in filters_available:
        filtered_image = apply_filter(file, filter)
    elif filter in custom_filters:
        filtered_image = apply_custom_filter(file, filter)
    return send_file(filtered_image, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run()
    