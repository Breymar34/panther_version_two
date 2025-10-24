from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load model and metrics
model_bundle = joblib.load("gwa_model_edited.pkl")
model = model_bundle["model"]
metrics = model_bundle["metrics"]

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    rq = None
    mae = None
    rmse = None

    # Default empty form values
    form_data = {
        "SHS_ENGLISH": "",
        "SHS_MATH": "",
        "SHS_SCIENCE": "",
        "SHS_GRADE": "",
        "EXAM": "",
        "track": "",
        "gender": "",
        "school_attended": "",
        "course": ""
    }

    if request.method == "POST":
        # Capture inputs
        form_data = request.form.to_dict()

        try:
            shs_english = float(request.form["SHS_ENGLISH"])
            shs_math = float(request.form["SHS_MATH"])
            shs_science = float(request.form["SHS_SCIENCE"])
            shs_grade = float(request.form["SHS_GRADE"])
            exam = float(request.form["EXAM"])

            track = request.form["track"]
            gender = request.form["gender"]
            school_attended = request.form["school_attended"]
            course = request.form["course"]

            # One-hot encode Track
            track_options = ["ABM", "BASICED", "GAS", "HUMSS", "STEM", "TVL"]
            track_encoded = [1 if track == opt else 0 for opt in track_options]

            # Encode Gender (Male=0, Female=1)
            gender_encoded = [0] if gender == "Male" else [1]

            # Encode School Attended (Private=0, Public=1)
            school_encoded = [0] if school_attended == "Private" else [1]

            # One-hot encode Course
            course_options = [
                "BEEd", "BPEd", "BSA", "BSBA", "BSBio", "BSCS", "BSCpE", "BSCrim",
                "BSECE", "BSEE", "BSEd", "BSHM", "BSIT", "BSInfo", "BSOA", "BSPsych",
                "BSTM", "BTLEd", "BTVTEd"
            ]
            course_encoded = [1 if course == opt else 0 for opt in course_options]

            # Final feature vector
            features = [[
                shs_english, shs_math, shs_science, shs_grade, exam,
                *track_encoded,
                *gender_encoded,
                *school_encoded,
                *course_encoded
            ]]

            prediction = model.predict(features)[0]
            prediction = round(prediction, 2)
            rq = metrics["rq"]
            mae = metrics["mae"]
            rmse = metrics["rmse"]

        except Exception as e:
            prediction = f"Error: {e}"

    return render_template("index.html", 
                           prediction=prediction,
                           rq=rq,
                           mae=mae,
                           rmse=rmse,
                           form_data=form_data)


# Important for Vercel
if __name__ == "__main__":
# app.run(debug=True, port=5001)
 app.run()    
