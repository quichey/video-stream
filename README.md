# 🎥 Video-Stream: Full-Stack System Architecture

A high-performance web application inspired by YouTube, engineered to demonstrate **scalable cloud architecture**, **asynchronous data flows**, and **complex session management**.

> **Note on Live Demo:** To optimize infrastructure costs, the live Azure deployment is currently offline. A **video walkthrough** of the system's functionality and architectural deep-dive is available below.

---

## 🏗️ Technical Highlights

This project serves as a technical showcase for replicating large-scale web technologies. Key engineering challenges addressed include:

* **Optimized Data Retrieval:** Implemented **infinite scrolling** for comments using efficient pagination logic and API design to minimize payload size and database strain.
* **Hybrid Session Management:** Developed a robust system to handle **anonymous, session-based, and authenticated (Google Auth) users** using secure cookies and temporary session tokens.
* **Scalable Storage Schema:** Engineered the backend to handle **video metadata and storage** (integrating with Azure Blob Storage) while maintaining schema flexibility for future scalability.
* **Cloud-Native Deployment:** Containerized the entire stack using **Docker** for consistent environments across development and production.

---

## 🛠️ Tech Stack

* **Frontend:** React (Context API + Hooks)
* **Backend:** Python (Flask)
* **Database:** SQLAlchemy + MySQL (Relational modeling for high-concurrency)
* **Infrastructure:** Docker + Azure (Container Apps & Blob Storage)
* **Authentication:** Google OAuth 2.0 + Secure Session Handling

---

## 📺 System Walkthrough & Demo

Since the live environment is archived, you can view the full functionality and architectural overview here:

https://github.com/user-attachments/assets/e3d97e09-b5ad-4864-b0e3-babe0284748b

*Features demonstrated in the video:*
* Video upload and playback streaming.
* Infinite scroll performance.
* User profile and session persistence.

---

## 🧑‍💻 Engineering Design Notes

This application was built as an iterative exploration of large-scale system design.
- **Comment Systems:** Focused on sub-second response times for deeply nested or high-volume comment threads.
- **Relational Mapping:** Designed dynamic row-mapping concepts (drawing from experience at **CliniComp**) to model hierarchical data structures efficiently.

For a deeper look into the design decisions, see **[DEV_NOTES.md](./DEV_NOTES.md)**.
