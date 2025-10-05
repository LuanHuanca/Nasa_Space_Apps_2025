# 🌌 ExoSky Navigator - NASA Space Apps Challenge 2025

> **"A World Away: Hunting for Exoplanets with AI"**

[![NASA Space Apps Challenge](https://img.shields.io/badge/NASA-Space%20Apps%20Challenge%202025-blue?style=for-the-badge&logo=nasa)](https://spaceappschallenge.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0-4FC08D?style=for-the-badge&logo=vue.js)](https://vuejs.org/)
[![Three.js](https://img.shields.io/badge/Three.js-WebGL-000000?style=for-the-badge&logo=three.js)](https://threejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-AI%20Backend-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

## 🎯 Challenge Overview

**ExoSky Navigator** is an innovative AI-powered exoplanet observation and discovery platform developed for the NASA Space Apps Challenge 2025. Our solution addresses the challenge of making exoplanet hunting accessible to everyone through an immersive 3D interactive experience.

### 🚀 The Problem We're Solving

- **Complexity**: Exoplanet data is often inaccessible to the general public
- **Visualization**: Current tools lack immersive 3D visualization capabilities
- **Education**: Limited interactive platforms for learning about exoplanets
- **Discovery**: Need for AI-assisted exoplanet detection and analysis

## ✨ Key Features

### 🌍 **Interactive Solar System**
- **3D Solar System Visualization** with realistic planet textures and orbits
- **Particle Star Field** using real NASA exoplanet coordinate data
- **Planet Navigation** - Click on planets to explore detailed information
- **Dynamic Animations** with orbital mechanics simulation

### 🔭 **Advanced Exoplanet Observer**
- **Location-Based Observation** - Select any point on Earth for observation
- **360° Horizon View** - Stellarium-like interface for sky observation
- **Real-time Exoplanet Detection** using AI algorithms
- **Interactive 3D Earth Globe** with pin placement for observation sites

### 🤖 **AI-Powered Discovery Engine**
- **Machine Learning Pipeline** for exoplanet habitability analysis
- **NASA Kepler Data Integration** with real astronomical coordinates
- **Intelligent Filtering** based on observation location and time
- **Predictive Analytics** for exoplanet visibility

### 💬 **AI Assistant Integration**
- **Google Gemini AI** integration for each planet
- **Contextual Information** about celestial bodies
- **Educational Content** delivery through conversational AI
- **Real-time Q&A** about astronomy and space exploration

## 🛠️ Technical Architecture

### **Frontend Stack**
```
Vue.js 3 + Composition API
├── Three.js - 3D Graphics & WebGL Rendering
├── Vite - Build Tool & Dev Server
├── Vue Router - SPA Navigation
└── Modular Component Architecture
```

### **Backend Stack**
```
FastAPI + Python
├── Machine Learning - Scikit-learn, NumPy, Pandas
├── NASA Data Integration - Real Kepler Mission Data
├── RESTful API - Exoplanet Discovery Endpoints
└── AI Processing Pipeline
```

### **Data Sources**
- **NASA Kepler Mission** - Confirmed exoplanet catalog
- **Exoplanet Archive** - Real astronomical coordinates
- **Stellarium Database** - Star positioning data
- **Custom AI Models** - Habitability scoring algorithms

## 🎮 User Experience Flow

1. **🏠 Solar System Exploration**
   - Interactive 3D solar system with realistic physics
   - Click planets to access detailed information
   - AI assistant available for each celestial body

2. **🌍 Earth Selection & Location Setup**
   - 3D Earth globe with realistic textures
   - Click anywhere to set observation location
   - Coordinate display and confirmation system

3. **🌅 Horizon View Observatory**
   - 360° panoramic sky view from selected location
   - Real-time exoplanet positioning based on coordinates
   - Interactive controls for sky navigation

4. **🔍 Exoplanet Discovery**
   - AI-powered detection of visible exoplanets
   - Habitability scoring and analysis
   - Detailed information panels for each discovery

## 🚀 Installation & Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### Frontend Setup
```bash
# Clone the repository
git clone https://github.com/LuanHuanca/Nasa_Space_Apps_2025.git
cd Nasa_Space_Apps_2025

# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend API Setup
```bash
# Navigate to API directory
cd Api

# Install Python dependencies
pip install -r ../requirements.txt

# Start FastAPI server
python main.py
```

### Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Add your Google Gemini AI API key
GEMINI_API_KEY=your_gemini_api_key_here
```

## 📁 Project Structure

```
ExoSky Navigator/
├── 🎨 Frontend (Vue.js)
│   ├── src/
│   │   ├── views/
│   │   │   ├── home.vue                    # Solar System 3D View
│   │   │   └── planets/earth/
│   │   │       ├── earth.vue               # Earth Detail View
│   │   │       └── ExoplanetObserver.vue   # Main Observatory
│   │   ├── components/exoplanet/
│   │   │   ├── WorldMap.vue               # 3D Earth Globe
│   │   │   ├── HorizonViewer.vue          # 360° Sky View
│   │   │   ├── ExoplanetList.vue          # Discovery Results
│   │   │   └── ChatAssistant.vue          # AI Integration
│   │   └── services/
│   │       └── ExoplanetAPIService.js     # API Communication
│   └── assets/                            # Textures & Resources
├── 🤖 Backend (FastAPI)
│   ├── main.py                            # API Server
│   ├── models/                            # ML Models
│   └── data/                              # NASA Datasets
└── 📊 Documentation
    ├── README.md                          # This file
    └── *.md                               # Technical docs
```

## 🔬 AI & Machine Learning Features

### **Exoplanet Detection Algorithm**
- **Input**: Observer location (lat/lng), time, viewing direction
- **Processing**: NASA Kepler database correlation with visibility calculations
- **Output**: List of potentially visible exoplanets with habitability scores

### **Habitability Scoring**
```python
Factors Considered:
├── Distance from host star (Habitable Zone)
├── Planet radius and mass
├── Stellar characteristics
├── Orbital parameters
└── Atmospheric potential
```

### **Real-time Coordinate Conversion**
- **Celestial Mechanics**: Converting exoplanet coordinates to observer's horizon view
- **Time-based Positioning**: Real-time sky position calculations
- **Visibility Prediction**: AI-powered visibility analysis based on location

## 🌟 Innovation Highlights

### **🎯 NASA Challenge Alignment**
- ✅ **Accessibility**: Makes exoplanet hunting accessible to everyone
- ✅ **Education**: Interactive learning through 3D visualization
- ✅ **AI Integration**: Machine learning for discovery assistance
- ✅ **Real Data**: Uses authentic NASA mission data

### **🚀 Technical Innovation**
- **3D Web Technology**: Advanced Three.js implementation
- **Real-time Processing**: FastAPI backend with ML pipeline
- **Modular Architecture**: Scalable Vue.js component system
- **Cross-platform**: Works on desktop, tablet, and mobile

### **🎨 User Experience Innovation**
- **Intuitive Interface**: No astronomy knowledge required
- **Immersive Experience**: Feel like a real astronomer
- **AI Guidance**: Contextual help and information
- **Progressive Discovery**: Gradual learning curve

## 🏆 NASA Space Apps Challenge Impact

### **Educational Value**
- Democratizes access to exoplanet science
- Encourages STEM education through interactive exploration
- Provides authentic NASA data experience

### **Scientific Contribution**
- Promotes citizen science in exoplanet discovery
- Creates public interest in space exploration
- Demonstrates practical AI applications in astronomy

### **Technical Achievement**
- Showcases modern web technologies for space education
- Integrates multiple data sources into cohesive experience
- Demonstrates scalable architecture for space applications

## 👥 Team & Development

**Developed for NASA Space Apps Challenge 2025**
- **Challenge Track**: A World Away: Hunting for Exoplanets with AI
- **Development Period**: October 2025
- **Tech Stack**: Vue.js 3, Three.js, FastAPI, AI/ML

## 🔗 Links & Resources

- **Live Demo**: [ExoSky Navigator](your-demo-link)
- **NASA Challenge**: [A World Away Challenge](https://spaceappschallenge.org/)
- **GitHub Repository**: [Source Code](https://github.com/LuanHuanca/Nasa_Space_Apps_2025)
- **Documentation**: [Technical Docs](./docs)

## 📄 License

This project was developed for the NASA Space Apps Challenge 2025. See the [NASA Space Apps Challenge Terms](https://spaceappschallenge.org/terms/) for more information.

---

**🌌 "Bringing the universe closer to humanity, one exoplanet at a time."**

*Made with ❤️ for NASA Space Apps Challenge 2025*
