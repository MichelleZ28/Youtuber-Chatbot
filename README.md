# 🎥 YouTuber Chatbot

A modern web application that lets you chat with an AI assistant trained on your favorite YouTuber's content. Experience natural conversations that mimic the style and knowledge of popular content creators.

![Image](https://github.com/user-attachments/assets/6f4b394f-21fc-4981-807a-200c8a5d09ef)

![Image](https://github.com/user-attachments/assets/d1f4c449-db13-4263-b4ff-b70661947c4f)

![Image](https://github.com/user-attachments/assets/9d6a5cf2-1d8e-4c79-b4dd-1012055e6a7f)

## ✨ Features

- **YouTube Channel Integration**: Connect with any YouTube channel using URL or handle
- **AI-Powered Chat**: Get responses that match the style and knowledge of the YouTuber

## 🚀 Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Python 3.11 (for backend)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/youtuber-chatbot.git
   cd youtuber-chatbot
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Environment Variables**
   Create `.env` files in both `frontend` and `backend` directories with the required variables (see `.env.example` files for reference).

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Start the frontend development server**
   ```bash
   cd frontend
   npm run dev
   ```

3. Open [http://localhost:5173](http://localhost:5173) in your browser.

## 🛠️ Tech Stack

- **Frontend**: 
  - React 18 with TypeScript
  - Chakra UI for styling
  - React Query for data fetching
  - Vite for build tooling

- **Backend**:
  - FastAPI
  - Python 3.11
  - SQLAlchemy (if using a database)
  - YouTube Data API

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Chakra UI](https://chakra-ui.com/) for the amazing component library
- [React](https://reactjs.org/) for the frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend
- All the open-source libraries that made this project possible
