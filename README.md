# EduGen AI - Intelligent Study Assistant

A comprehensive AI-powered study platform that helps students learn efficiently through document analysis, interactive Q&A, quiz generation, and learning analytics.

## 🎯 Features

- **Document Upload & Management**: Upload PDF, DOCX, PPTX files
- **AI Study Assistant**: Ask questions about uploaded materials with RAG-powered answers
- **Quiz Generation**: Auto-generate MCQs, True/False, and essay questions
- **Flashcard Creator**: Automatically create study flashcards
- **Study Planner**: Generate personalized study schedules
- **Analytics Dashboard**: Track progress with charts and insights
- **Learning Modes**: Beginner, Intermediate, and Advanced explanations
- **Search**: Global search across documents, notes, and flashcards

## 🛠️ Tech Stack

### Frontend
- React.js (Vite)
- Tailwind CSS
- React Router
- Axios

### Backend
- Python FastAPI
- PostgreSQL with SQLAlchemy ORM
- LangChain & ChromaDB for RAG
- OpenAI API integration
- JWT Authentication

### DevOps
- Docker & Docker Compose
- Environment-based configuration

## 📁 Project Structure

```
EduGen-AI/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── api/
│   ├── auth/
│   ├── ai/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── uploads/
│   ├── utils/
│   ├── main.py
│   └── requirements.txt
├── docs/
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 16+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abhijitpikun559-design/Abhijit.git
   cd Abhijit
   git checkout edugen-ai-main
   ```

2. **Setup Environment Variables**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Installation

**Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

## 📚 Database Schema

- **Users**: User accounts and profiles
- **Subjects**: Subject categories
- **Documents**: Uploaded study materials
- **DocumentChunks**: Indexed document chunks for RAG
- **Flashcards**: Auto-generated flashcards
- **Quiz**: Quiz metadata
- **QuizQuestions**: Individual quiz questions
- **QuizResponses**: User quiz answers
- **Progress**: Learning progress tracking
- **StudySessions**: Study session logs
- **Notifications**: User notifications

## 🔐 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- File upload validation
- SQL injection prevention
- XSS protection
- CORS configuration
- Rate limiting

## 📖 API Documentation

Full API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 Environment Variables

See `.env.example` files in both frontend and backend directories for required configuration.

## 🤝 Contributing

Contributions are welcome! Please follow the code style and submit pull requests.

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Developed as a comprehensive AI study assistant platform.

## 📞 Support

For issues and questions, please open an issue on GitHub.
