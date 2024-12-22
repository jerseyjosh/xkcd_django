# XKCD Comics Database with Semantic Search

## Overview
This project is a Django app designed to maintain a **searchable database of XKCD comics**. It supports **semantic search** by generating **OpenAI embeddings** for each comic.
---

## Features
- **Fetch XKCD Comics**: Retrieve comics asynchronously with http requests.
- **Database Management**: Stores comics, including metadata (title, alt text, transcript) and publish dates.
- **OpenAI Embeddings**: Generates embeddings for transcripts to enable semantic similarity searches.
- **Semantic Search**: Uses cosine similarity to find comics related to user queries.

---

## Setup Instructions

### **1. Clone the Repository**
```bash
git clone <repo-url>
cd xkcd_comics
```

### **2. Set Up Environment Variables**
Create a `.env` file and add the following:
```
OPENAI_API_KEY=<your-openai-api-key>
```

### **3. Apply Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **4. Create a Superuser** (for admin access)
```bash
python manage.py createsuperuser
```

### **5. Run the Server**
```bash
python manage.py runserver
```

---

## Usage

### **Fetching XKCD Comics**

1. **Fetch All Comics:**
```bash
python manage.py fetch_comics
```

2. **Fetch the Latest Comic:**
```bash
python manage.py fetch_comics --latest
```

3. **Fetch Comics by Range:**
```bash
python manage.py fetch_comics --range 1 100
```

4. **Update Comics:**
```bash
python manage.py fetch_comics --update
```

---

### **Generate Embeddings**
To generate embeddings for comics missing them:
```bash
python manage.py generate_embeddings
```

---

### **Semantic Search**
Search for the most relevant comics based on meaning:
```bash
python manage.py search_comics "time travel"
```
Example Output:
```
Searching for: time travel

Top 5 Results:
#123: Relativity
  Similarity: 0.9123
  URL: https://imgs.xkcd.com/comics/relativity.png
  Alt Text: Time dilation explained humorously.
```