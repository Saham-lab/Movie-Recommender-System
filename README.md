

# 🎬 Movie Recommender System  

A simple **Movie Recommendation Web App** built using **Streamlit** and **Python**.  
It suggests similar movies based on user selection and displays movie posters fetched from the **OMDb API**.

---

## 🚀 Features  
- 🔍 Search or select a movie from the dropdown list  
- 🎞️ Get **8 recommended movies** similar to your choice  
- 🖼️ Movie posters automatically fetched using the **OMDb API**  
- ⚡ Fast and interactive UI built with **Streamlit**

---

## 🧠 How It Works  
1. A pre-trained similarity model (`similarity.pkl`) computes how close each movie is to another.  
2. When you select a movie, the app finds the top similar ones.  
3. Poster images are fetched in real-time from the [OMDb API](https://www.omdbapi.com/).

---

## 📂 Project Structure  
```

movie-recommender-system/
├── app.py               # Main Streamlit application
├── requirements.txt     # List of dependencies
├── movie_list.pkl       # Pickle file containing movie data , the file in the google drive
├── similarity.pkl       # Pickle file containing similarity matrix, the file in the google drive
└── README.md            # Project documentation

````

---

## ⚙️ Installation & Setup  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/Saham-lab/Movie-Recommender-System.git
cd Movie-Recommender-System
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Streamlit app

```bash
streamlit run app.py
```

Once it starts, open the URL displayed in your terminal — usually:
👉 [http://localhost:8501](http://localhost:8501)

---

## ☁️ Deployment (Optional)

If your `.pkl` files are too large for GitHub, upload them to **Google Drive** and download them dynamically in your app using `gdown`:

```python
import gdown

gdown.download("https://drive.google.com/uc?id=YOUR_FILE_ID", "similarity.pkl", quiet=False)
gdown.download("https://drive.google.com/uc?id=YOUR_FILE_ID", "movie_list.pkl", quiet=False)
```

---

## 🧰 Requirements

* Python 3.8 or higher
* Streamlit
* Pandas
* NumPy
* scikit-learn
* requests
* pickle

---

## 💡 Future Improvements

* Add user-based collaborative filtering
* Include movie genres, ratings, and overviews
* Enhance UI with Streamlit components

---

## 📜 License

This project is open-source under the **MIT License**.

Built with ❤️ using **Python** and **Streamlit**.

