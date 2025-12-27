# NewsScope

News Analyzer is a modular data science application designed to ingest, analyze, and interpret news articles at scale.  
The system focuses on **clickbait detection**, **content summarization**, and **bias analysis**, implemented using a clean, service-oriented architecture.

This project represents a structured transition from an experimental machine learning prototype to a maintainable, production-style codebase, with emphasis on separation of concerns, extensibility, and reproducibility.

---

## Clickbait Detection Approach

The clickbait detection module uses a hybrid strategy combining multiple signals:

- Feature-based classification using Logistic Regression  
- Semantic similarity between headline and article content using embeddings  
- Hybrid decision logic that integrates both signals for robust predictions  

---

## Key Capabilities

- Automated news ingestion pipeline using NewsAPI  
- Hybrid clickbait detection leveraging statistical and semantic features  
- Extractive text summarization for concise content understanding  
- Service-layer abstraction to decouple ML logic from the UI  
- Interactive Streamlit interface for exploration and analysis  
- Structured project layout aligned with industry best practices  

---

## Project Architecture

```text
News_Analyzer/
│
├── app/
│   ├── collector/              # External data ingestion (NewsAPI)
│   ├── services/               # Service layer
│   │   ├── news_service.py
│   │   ├── clickbait_service.py
│   │   └── summarization_service.py
│   │
│   ├── models/                 # ML / NLP models (scaffolded)
│   │   ├── clickbait/
│   │   └── summarizer/
│   │
│   ├── pages/                  # Streamlit pages
│   └── app.py                  # Streamlit entry point
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── artifacts/
│
├── docker/                     # Docker support (future)
├── requirements.txt
├── README.md
└── .gitignore
```


---

## Notes on Structure

- **collector/**  
  Handles external data ingestion and API communication.

- **services/**  
  Acts as the application’s core layer, exposing clean interfaces for news fetching, clickbait detection, and summarization.

- **models/**  
  Contains machine learning and NLP logic. Currently scaffolded to support incremental migration from experimental code.

- **pages/**  
  Streamlit UI components for interactive exploration.

- **data/**  
  Organized storage for raw inputs, processed datasets, and model artifacts.

This structure follows service-oriented design principles and enables scalability without tightly coupling UI, data ingestion, and ML logic.

---

## Author

## Indrayani Parande    

Data Science Undergraduate with a focus on Machine Learning and Natural Language Processing.
