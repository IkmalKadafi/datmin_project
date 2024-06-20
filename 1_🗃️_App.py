import numpy as np
import pickle
import streamlit as st

st.set_page_config(
    page_title="Data Mining PJBL",
    page_icon="💻",
)

st.sidebar.success("Select a page above")

# Load Model
loaded_model = pickle.load(open('Data/model1.sav', 'rb'))

# Creating a function for prediction
def ipm_prediction(input_data):
    # Testing Saved Model
    input_data_array = np.asarray(input_data)

    input_data_reshaped = input_data_array.reshape(1, -1)
    
    if not np.all(np.isfinite(input_data_reshaped)):
        raise ValueError("Input data contains NaN or Inf values")

    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)

    if (prediction[0] >= 80):
        return f"prediction: {prediction[0]}\nKelas : Sangat Tinggi"
    elif (prediction[0] >= 70 and prediction[0] < 80):
        return f"prediction: {prediction[0]}\nKelas : Tinggi"
    elif (prediction[0] >= 60 and prediction[0] < 70):
        return f"prediction: {prediction[0]}\nKelas : Sedang"
    else:
        return f"prediction: {prediction[0]}\nKelas : Rendah"


def main():
    # Giving a tittle
    st.title("App Prediksi Indeks Pembangunan Manusial (IPM)")

    # Giving Input  data
    uhh = st.text_input("Masukkan Nilai Umur Harapan Hidup (tahun)")
    hls = st.text_input("Masukkan Nilai Harapan Lama Sekolah (tahun)")
    rls = st.text_input("Masukkan Nilai Rata-Rata Lama Sekolah (tahun)")
    ppk = st.text_input("Masukkan Nilai Pengeluaran Per Kapita (ribu rupiah)")

    # Prediction Class
    ipm_predict = ''

    # create button for predict
    if st.button('IPM Prediction Result'):
        ipm_predict = ipm_prediction([uhh, hls, rls, ppk])

    st.success(ipm_predict)



if __name__ == '__main__':
    main()
