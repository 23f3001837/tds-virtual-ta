# Virtual Teaching Assistant for TDS (Tools in Data Science) - Jan 2025

This project is a **FastAPI-based Virtual Teaching Assistant** for answering student queries related to the **Tools in Data Science (TDS)** course offered by **IIT Madras**. It uses scraped data from the IITM Online Degree **Discourse** forum and the official **course content** website. Answers are generated using a Large Language Model (LLM) via **AIPipe API** with **retrieval-augmented generation (RAG)** for better relevance.

---

## Features

- ✅ Answers TDS course-related questions using relevant **Discourse posts** and **official course content**.
- ✅ Uses **TF-IDF + Cosine Similarity** for content retrieval.
- ✅ Generates answers via **AIPipe LLM API**.
- ✅ Returns relevant links to **Discourse threads** and **course content**.
- ✅ Built with **FastAPI** for rapid deployment.
- ✅ Timeout of **20 seconds** for search + generation to prevent hanging.

---
