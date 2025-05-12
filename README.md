# Cyberstalking Awareness Portal 🌐🛡️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
![Project Version](https://img.shields.io/badge/version-1.14-blue)

A comprehensive platform for reporting and tracking cyberstalking incidents, with educational resources and support features.

## 🚀 Quick Start

### 1. **Clone the repository**
```bash
git clone https://github.com/yuvrajsharmaaa/Cyber_Stalk.git
cd Cyber_Stalk
```

### 2. **Set up Python environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Configure the project**
- Copy `config.cfg.example` to `config.cfg` and update the settings
- Set up your database connection in `settings.py`

### 5. **Run the development server**
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to access the portal.

## 🛠 Tech Stack

### Frontend
- HTML5 & CSS3
- Tailwind CSS
- Vanilla JavaScript
- Material Design Icons

### Backend
- FastAPI
- SQLAlchemy ORM
- Uvicorn
- Aquilify Framework

### Database
- PostgreSQL (default)
- Support for other SQL databases

## 📝 Core Features

- 🔒 Anonymous incident reporting
- 📤 Secure file upload system
- 📊 Admin dashboard for report management
- 🎓 Educational resources
- 🛡️ Digital safety guides
- 🤝 Support community integration

## 🛡️ Security Features

- End-to-end encryption for sensitive data
- Secure file upload handling
- Rate limiting and DDoS protection
- Environment-based configuration
- Regular security audits

## 📁 Project Structure

```
Cyber_Stalk/
├── api/            # API endpoints
├── app/           # Application core
├── assets/        # Static assets
├── config/        # Configuration files
├── models/        # Database models
├── public/        # Public static files
├── Routes/        # Route definitions
├── src/           # Source code
├── uploads/       # User uploads
└── venv/          # Virtual environment
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All contributors who have helped shape this project
- The open-source community for their invaluable tools and resources

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

Made with ❤️ by [Yuvraj Sharma](https://github.com/yuvrajsharmaaa)
