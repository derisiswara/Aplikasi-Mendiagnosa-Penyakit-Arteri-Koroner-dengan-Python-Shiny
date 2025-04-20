import shiny
from shiny import ui, render, reactive
import pandas as pd
import joblib
import numpy as np

# Load the logistic regression model
model_old = joblib.load("logreg_py.joblib")

# Define UI
app_ui = ui.page_fluid(
    ui.h2("Aplikasi Mendiagnosa Penyakit Arteri Koroner", class_="text-center mb-4"),

    # Define layout with two columns for the inputs
    ui.row(
        ui.column(6,  # 6/12 = 50% of the width
            ui.input_numeric("num1", "Usia (age)", min=0, value=1)
        ),
        ui.column(6,  # 6/12 = 50% of the width
            ui.input_select("select2", "Jenis Kelamin (sex)", choices=["Perempuan", "Laki-laki"], selected="Laki-laki")
        )
    ),
    ui.row(
        ui.column(6,
            ui.input_select("select3", "Jenis Nyeri Dada (cp)",
                            choices=["Angina Tipikal", "Angina Atypical", "Nyeri Non-Anginal", "Asimptomatik"], selected="Angina Tipikal")
        ),
        ui.column(6,
            ui.input_numeric("num4", "Tekanan Darah (trestbps)", value=120, min=0)
        )
    ),
    ui.row(
        ui.column(6,
            ui.input_numeric("num5", "Kolesterol (choi)", value=200, min=0)
        ),
        ui.column(6,
            ui.input_select("select6", "Gula Darah Puasa (fbs)", choices=["Tidak", "Ya"], selected="Ya")
        )
    ),
    ui.row(
        ui.column(6,
            ui.input_select("select7", "EKG pada Istirahat (restecg)",
                            choices=["Normal", "Kelainan ST-T", "Hipertrofi Ventrikel Kiri"], selected="Normal")
        ),
        ui.column(6,
            ui.input_numeric("num8", "Denyut Jantung Maksimal (thalach)", value=150, min=0)
        )
    ),
    ui.row(
        ui.column(6,
            ui.input_select("select9", "Angina pada Latihan (exang)", choices=["Tidak", "Ya"], selected="Tidak")
        ),
        ui.column(6,
            ui.input_numeric("num10", "Depresi ST pada Latihan (oldpeak)", value=1, min=0)
        )
    ),
    ui.row(
        ui.column(6,
            ui.input_select("select11", "Kemiringan Segmen ST (slope)", choices=["Menanjak", "Datar", "Menurun"], selected="Menanjak")
        ),
        ui.column(6,
            ui.input_select("select12", "Jumlah Pembuluh Darah (ca)", choices=["0", "1", "2", "3"], selected="0")
        )
    ),
    ui.row(
        ui.column(12,
            ui.input_select("select13", "Thallium Stress Test (thai)",
                            choices=["Normal", "Defek Tetap", "Defek yang Dapat Dipulihkan"], selected="Normal")
        )
    ),
    ui.row(
        ui.column(12,  # Full width column for the submit button
            ui.input_action_button("submitBtn", "Submit", class_="btn btn-primary", width="100%")
        )
    ),
    
    ui.row(
        ui.column(12,
            ui.output_text_verbatim("value")
        )
    ),
    
    # Add a bit of spacing and padding to the main panel
    ui.tags.style("""
        .shiny-input-container { margin-bottom: 15px; }
        .shiny-input-action-button { margin-top: 20px; }
        .container { padding-top: 30px; }
    """)
)

# Define Server Logic
def server(input, output, session):
    
    # Initially, hide output and only show after the submit button is clicked
    @output
    @render.text
    def value():
        # Do nothing until the submit button is pressed
        if input.submitBtn() == 0:
            return ""
        
        # Prepare data for prediction
        data = pd.DataFrame({
            'age': [input.num1()],
            'sex': [1 if input.select2() == "Laki-laki" else 0],
            'cp': [["Angina Tipikal", "Angina Atypical", "Nyeri Non-Anginal", "Asimptomatik"].index(input.select3()) + 1],
            'trestbps': [input.num4()],
            'choi': [input.num5()],
            'fbs': [1 if input.select6() == "Ya" else 0],
            'restecg': [["Normal", "Kelainan ST-T", "Hipertrofi Ventrikel Kiri"].index(input.select7())],
            'thalach': [input.num8()],
            'exang': [1 if input.select9() == "Ya" else 0],
            'oldpeak': [input.num10()],
            'slope': [["Menanjak", "Datar", "Menurun"].index(input.select11()) + 1],
            'ca': [int(input.select12())],
            'thai': [["Normal", "Defek Tetap", "Defek yang Dapat Dipulihkan"].index(input.select13()) + 3]
        })

        # Make prediction using the model pipeline
        pred = model_old.predict(data)[0]

        # Display prediction result
        if pred == 1:
            return "Terdiagnosa Penyakit Arteri Koroner"
        else:
            return "Tidak Terdiagnosa Penyakit Arteri Koroner"

# Create the app instance
app = shiny.App(app_ui, server)

# Run the Shiny app
if __name__ == "__main__":
    app.run()
