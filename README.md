
# MindNest - Mental Health Support App

MindNest is a full-stack mental health app that includes:
- 🧠 Therapist chatbot with crisis detection
- 🎮 Text-based therapeutic sci-fi game
- 📚 Audiobooks, 🎵 calming songs, 🧘 coping strategies
- 📅 Appointment scheduling, 💊 medication tracking
- 👨‍👧 Guardian profiles, Zoom Movie Night, Open Mic

## 🛠️ Project Structure

```
mindnest/
├── backend/          # Flask API
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit_app.py  # Optional retro UI
│   └── react-ui/         # React classic OS interface
│       ├── src/
│       │   ├── App.jsx
│       │   ├── App.css
│       │   └── components/
│       │       ├── Sidebar.jsx
│       │       ├── Messages.jsx
│       │       ├── Appointments.jsx
│       │       ├── Medication.jsx
│       │       └── ZoomMeetings.jsx
│       ├── public/
│       └── package.json
│
├── .gitignore
└── README.md
```

## 🚀 Deployment Options

### Backend (Flask)
- Host on [Render.com](https://render.com)
- Python Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`

### Frontend (React)
- Host on [Vercel](https://vercel.com)
- Root: `frontend/react-ui`
- Add `.env`:
  ```
  REACT_APP_API_URL=https://your-backend-url.onrender.com
  ```

## 💡 Future Plans
- PostgreSQL + Auth
- User reflections log
- Community journaling and chat rooms
