# BookWise - Django Book Recommendation System

![BookWise Logo](https://via.placeholder.com/150?text=BW)  
*Personalized book discovery platform*

## 📖 Overview
BookWise is a Django-based web application that provides personalized book recommendations using collaborative filtering and content-based algorithms. This capstone project demonstrates a full-stack implementation of a recommendation system with user management, book catalog, and machine learning integration.

## ✨ Key Featuresgit 
### Recommendation Engine
- **Hybrid filtering** combining:
  - Collaborative filtering (user-item interactions)
  - Content-based filtering (book metadata)
- Popularity-based suggestions
- "Readers who liked this also liked..." recommendations

### User Experience
- 👤 User registration and profiles
- 📚 Personal bookshelf (read/reading/to-read)
- ⭐ Rating system (1-5 stars)
- ❤️ Wishlist functionality
- 🔍 Advanced search and filtering

### Admin Features
- 📊 Dashboard with usage analytics
- 📥 Bulk book import (CSV/JSON)
- ⚙️ Recommendation algorithm tuning
- 👥 User management tools

## 🛠️ Technology Stack
### Core Components
| Component          | Technology              |
|--------------------|-------------------------|
| **Backend**        | Django 5.2, Python 3.12 |
| **Database**       | PostgreSQL 14           |

### Frontend
- HTML5/CSS3 with Bootstrap 5
- JavaScript (ES6)
- Responsive design

##  Installation

### Prerequisites
- Python 3.12
- PostgreSQL 25.3
- Virtualenv

### Setup Instructions
1. Clone repository:
```bash
git clone https://github.com/yourusername/bookwise.git
cd bookwise