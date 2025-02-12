
# LinkedIn Job Application Bot  

This project is a **LinkedIn automation bot** built using **Python, Selenium, and Django**. The bot automatically applies for jobs on LinkedIn based on predefined criteria.  

## Features  

✅ Automated job searching and applying  
✅ Configurable job filters (title, location, etc.)  
✅ Uses Selenium for browser automation  
✅ Django-based backend for managing job applications  
✅ Docker support for easy deployment  

## Installation  

### Prerequisites  

- Python 3.x  
- Google Chrome and ChromeDriver  
- Docker (optional)  

### Setup  

1. Clone this repository:  
   ```bash
   git clone https://github.com/yourusername/linkedin-automation.git
   cd linkedin-automation
   ```  

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

3. Set up environment variables (e.g., LinkedIn credentials) in `.env` file:  
   ```plaintext
   LINKEDIN_EMAIL=your-email@example.com  
   LINKEDIN_PASSWORD=yourpassword  
   ```  

4. Run migrations:  
   ```bash
   python manage.py migrate
   ```  

5. Start the Django server:  
   ```bash
   python manage.py runserver
   ```  

## Usage  

1. Update **`additionalQuestions.yaml`** to define job search criteria.  
2. Run the bot:  
   ```bash
   python manage.py runbot
   ```  
3. The bot will automatically log in to LinkedIn and apply for relevant jobs.  

## Docker Deployment  

To run the bot using Docker:  
```bash
docker build -t linkedin-bot .  
docker run -d linkedin-bot  
```  

## Project Structure  

```
├── data/                   # Data storage  
├── joblink/                # Core bot logic  
├── Dockerfile              # Docker setup  
├── additionalQuestions.yaml # Job filtering rules  
├── build.sh                # Build script  
├── db.sqlite3              # SQLite database  
├── manage.py               # Django management script  
├── render.yaml             # Deployment config  
├── requirements.txt        # Python dependencies  
├── urls.py                 # Django URLs  
```  
