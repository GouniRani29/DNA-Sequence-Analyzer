from flask import Flask, request, jsonify

from transformer_predict import predict_gene_family


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "DNA Transformer ML API is running"
    })


# =========================================================
# DNA PREDICTION
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # -------------------------------------------------
        # GET REQUEST DATA
        # -------------------------------------------------

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Request body is empty"
            }), 400


        # -------------------------------------------------
        # GET DNA SEQUENCE
        # -------------------------------------------------

        sequence = data.get("sequence")


        if not sequence:

            return jsonify({
                "success": False,
                "message": "DNA sequence is required"
            }), 400


        # -------------------------------------------------
        # PREDICT
        # -------------------------------------------------

        result = predict_gene_family(
            sequence
        )


        # -------------------------------------------------
        # RETURN RESULT
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "sequence": sequence,

            "predictedClass":
                result["predictedClass"],

            "confidence":
                result["confidence"],

            "probabilities":
                result["probabilities"]

        })


    except ValueError as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 400


    except Exception as error:

        print("Prediction error:", error)

        return jsonify({

            "success": False,

            "message": "Prediction failed",

            "error": str(error)

        }), 500


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DNA TRANSFORMER FLASK API")
    print("=" * 60)

    print("\nStarting server...")
    print("URL: http://127.0.0.1:5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )