# SalesFinal
---

## 📩 Gmail API Integration Setup

To enable Gmail-based email and attachment summarization, follow these steps to configure your Gmail API credentials.

---

### ✅ Step 1: Enable Gmail API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a **new project** or select an existing one.
3. Navigate to **APIs & Services > Library**.
4. Search for **Gmail API** and click **Enable**.

---

### ✅ Step 2: Configure OAuth Consent Screen

1. Go to **APIs & Services > OAuth consent screen**.
2. Click **Create**
3. Fill in the **App name**, Choose **External** for user type, and fill in remaining details.
4. Click **Save and Continue** until the summary page.
5. Go to **Audience** in **OAuth consent screen** and below **Test Users** click **Add Users**
6. Enter the **email** of the one who will receive the tenders.
7. Go to **Data Access** in **OAuth consent screen**
8. In **Data Access** click **Add or remove scopes**.
9. Search or Select **.../auth/gmail.readonly**.
10. Scroll down and click on **Save**.

---

### ✅ Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials > OAuth Client ID**.
3. Choose:

   * **Application type**: Desktop App
   * **Name**: e.g., `TenderSummarizerClient`
4. Click **Create**.
5. Click **Download JSON** — this is your `credentials.json`.

### 🔐 Rename the file to `credentials.json` and place it in the **root of your project folder** (next to `Salesapp.py`).

---

### 📁 Project Folder Structure (Sample)

```
Sales2/
├── Salesapp.py
├── gmail_utils.py
├── credentials.json     ✅ Your downloaded credentials
├── token.json           🔒 Generated after first run
```
---

### ✅ Step 4: First-Time Authorization

1. Run **python gmail_utils.py** 
* A browser or link will open asking you to log in (**USING THE MAIL TO ADDED IN TEST USERS ABOVE**) and authorize the Gmail read access.
* After successful login u might see a **✅ Gmail authentication successful.** in your terminal and a `token.json` file will be generated — this securely stores your access and refresh tokens.
2. Run **streamlit run Salesapp.py**
* A list of **Sent and Received Emails** will be visible with a **Generate button** next to it

---

### ✅ Step 5: Streamlit Secrets
1. After deploying the app to Streamlit go to **My apps** -> Your app **Settings** -> **Secrets**
2. Put put your apikey, credentials.json and tokenjson details in the following format:
   *Fill in the "" with your own data obviously!
```toml
cohere_api_key=""

credentials = """
{
  "installed": {
    "client_id": "",
    "project_id": "",
    "auth_uri": "",
    "token_uri": "",
    "auth_provider_x509_cert_url": "",
    "client_secret": "",
    "redirect_uris": ["http://localhost"]
  }
}
"""

token = """
{
  "token": "",
  "refresh_token": "",
  "token_uri": "",
  "client_id": "",
  "client_secret": "",
  "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
  "universe_domain": "googleapis.com",
  "account": "",
  "expiry": ""
}
"""
```

---
# 🔄 Migrating from Cohere to OpenAI in `Salesapp.py`

This guide explains how to replace **Cohere API** with **OpenAI API** in your `Salesapp.py` for summarizing tenders and emails.

---

## ✅ Step 1: Install OpenAI Library

Install the required OpenAI Python package:

```bash
pip install openai
```

---

## ✅ Step 2: Update Imports

Replace the existing import of Cohere:

```python
import cohere
```

With:

```python
import openai
```

---

## ✅ Step 3: Set OpenAI API Key

Replace the Cohere client initialization:

```python
co = cohere.Client("your-cohere-key")
```

With:

```python
openai.api_key = "your-openai-api-key"
```

Or load it from `st.secrets` if using Streamlit:

```python
openai.api_key = st.secrets["openai_api_key"]
```

---

## ✅ Step 4: Update `stream_summary_from_cohere` Function

Replace the Cohere streaming logic:

```python
response = co.chat_stream(
    model="command-a-03-2025",
    message=prompt
)
for chunk in response:
    if hasattr(chunk, "text") and chunk.text:
        yield chunk.text
```

With OpenAI's streaming format:

```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    stream=True
)
for chunk in response:
    if "choices" in chunk and chunk["choices"][0].get("delta", {}).get("content"):
        yield chunk["choices"][0]["delta"]["content"]
```

---

## ✅ Step 5: Update `stream_email_summary_from_cohere` Similarly

Also replace the cohere streaming call in `stream_email_summary_from_cohere` with:

```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    stream=True
)
for chunk in response:
    if "choices" in chunk and chunk["choices"][0].get("delta", {}).get("content"):
        yield chunk["choices"][0]["delta"]["content"]
```

---

### ✅ Done
