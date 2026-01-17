# 🚀 Google Gemini Setup Guide

## ✅ Kya Change Hua?

Humne **OpenAI ko Google Gemini se replace kar diya hai!**

### Fayde:
- ✅ **FREE** - No payment required!
- ✅ **Fast** - Gemini 1.5 Flash bahut tez hai
- ✅ **Powerful** - Latest AI technology
- ✅ **Easy** - Simple setup

---

## 📝 Step-by-Step Setup

### Step 1: Gemini API Key Le Lo (FREE!)

1. **Website kholo**: https://aistudio.google.com/app/apikey

2. **Google account se login karo**

3. **"Create API Key" button click karo**

4. **API key copy karo** - Yeh aisa dikhega:
   ```
   AIzaSyAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

5. **Save kar lo** - Yeh key sirf ek baar dikhegi!

---

### Step 2: Backend Setup Karo

#### 1. Install Gemini Package

```bash
cd backend

# Activate virtual environment (agar hai)
venv\Scripts\activate

# Install Gemini SDK
pip install google-generativeai
```

#### 2. Update .env File

Edit `backend/.env` file:

```env
# Database URL (pehle jaisa hai, no change)
DATABASE_URL=postgresql://your-neon-url-here

# JWT Secret (pehle jaisa hai, no change)
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
REFRESH_TOKEN_EXPIRE_MINUTES=43200

# ⭐ NEW: Gemini API Key (OpenAI wala hata do)
GEMINI_API_KEY=AIzaSyAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=gemini-1.5-flash
MAX_CONVERSATION_MESSAGES=50

# Purani lines DELETE kar do:
# OPENAI_API_KEY=...
# OPENAI_MODEL=...
```

**Important:**
- `OPENAI_API_KEY` ko `GEMINI_API_KEY` se replace karo
- Apni actual Gemini API key paste karo

---

### Step 3: Backend Server Start Karo

```bash
cd backend

# Make sure virtual environment active hai
venv\Scripts\activate

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ **Backend ready!**

---

### Step 4: Frontend Start Karo (No Changes!)

Frontend mein koi change nahi hai:

```bash
cd frontend

# Start dev server
npm run dev
```

✅ **Frontend ready at http://localhost:3000**

---

## 🧪 Testing Karo

### Test Chat Feature:

1. **Login karo**: http://localhost:3000/login

2. **Chat page kholo**: Click "Chat" button in dashboard

3. **Message bhejo**:
   ```
   Add a task to buy milk
   ```

4. **AI response dekho**:
   ```
   I've added 'Buy milk' to your tasks.
   ```

5. **Try more commands**:
   ```
   Show me my tasks
   Complete task 1
   Delete task 2
   Add task to call dentist tomorrow
   ```

---

## 🎯 Gemini Models

### Available Models:

1. **gemini-1.5-flash** (Recommended - FREE)
   - Fast responses
   - Good for chat
   - Free tier: 15 requests/minute
   - ✅ Currently using this

2. **gemini-1.5-pro** (Powerful - FREE)
   - More accurate
   - Better reasoning
   - Free tier: 2 requests/minute

3. **gemini-1.0-pro** (Stable - FREE)
   - Older but stable
   - Free tier: 60 requests/minute

**Change Model:** Edit `.env`:
```env
GEMINI_MODEL=gemini-1.5-pro
```

---

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY not set"

**Fix:**
```bash
# Check .env file exists
cd backend
type .env

# Make sure it has:
GEMINI_API_KEY=AIzaSy...

# Restart backend
uvicorn app.main:app --reload
```

### Error: "API key invalid"

**Fix:**
1. Check API key spelling
2. Generate new key: https://aistudio.google.com/app/apikey
3. Update `.env` file
4. Restart backend

### Error: "Rate limit exceeded"

**Fix:**
- Gemini free tier has limits
- Wait 1 minute
- Or upgrade to paid tier (optional)

**Check limits:** https://ai.google.dev/pricing

---

## 📊 Comparison: OpenAI vs Gemini

| Feature | OpenAI | Gemini |
|---------|--------|--------|
| **Price** | Paid ($) | FREE ✅ |
| **Speed** | Fast | Very Fast ✅ |
| **Free Tier** | No | Yes ✅ |
| **Rate Limit** | Low (paid) | 15-60 req/min ✅ |
| **Tool Calling** | Yes | Yes ✅ |
| **Setup** | Credit card needed | Email only ✅ |

---

## ✅ Success Indicators

Sab kuch kaam kar raha hai jab:

✅ Backend starts without errors
✅ `.env` file mein `GEMINI_API_KEY` set hai
✅ Chat message bhejne par AI response aata hai
✅ Tasks create/update/delete ho rahe hain via chat
✅ No errors in backend logs
✅ Browser console mein `AI executed tools: [...]` dikhai de raha hai

---

## 🎉 Done!

Ab aap **FREE Gemini AI** use kar sakte ho!

### Test Commands:

```
"Add task to prepare presentation"
"Show all my pending tasks"
"Mark task 1 as complete"
"Delete completed tasks"
"Add task to buy groceries tomorrow"
"What tasks do I have?"
```

---

## 🆘 Help Chahiye?

Agar koi problem hai to:

1. **Backend logs check karo** - Terminal mein errors
2. **Browser console dekho** - F12 press karke
3. **API key verify karo** - https://aistudio.google.com/app/apikey
4. **Restart servers** - Backend aur frontend dono

---

## 📚 Resources

- **Gemini API Docs**: https://ai.google.dev/docs
- **Get API Key**: https://aistudio.google.com/app/apikey
- **Pricing**: https://ai.google.dev/pricing (FREE tier available!)
- **Rate Limits**: https://ai.google.dev/docs/quota

---

**Happy Coding with FREE Gemini AI! 🚀🎉**
