# 🎥 YouTuber Chatbot

A modern web application that lets you chat with an AI assistant trained on your favorite YouTuber's content. Experience natural conversations that mimic the style and knowledge of popular content creators.

![App Screenshot](https://via.placeholder.com/800x500.png?text=YouTuber+Chatbot+Screenshot)  
*Screenshot placeholder - replace with actual screenshot of your app*

## ✨ Features

- **YouTube Channel Integration**: Connect with any YouTube channel using URL or handle
- **AI-Powered Chat**: Get responses that match the style and knowledge of the YouTuber
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Built with Chakra UI for a clean, accessible interface
- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **Real-time Interaction**: Smooth, responsive chat experience

## 🚀 Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Python 3.8+ (for backend)

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
  - Python 3.8+
  - SQLAlchemy (if using a database)
  - YouTube Data API

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Chakra UI](https://chakra-ui.com/) for the amazing component library
- [React](https://reactjs.org/) for the frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend
- All the open-source libraries that made this project possible
