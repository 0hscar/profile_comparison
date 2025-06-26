# Business Profile Assistant

This project is a business profile comparator tool as an extension to an application. It allows users to compare their restaurant or business profile with nearby and similar businesses, leveraging AI-generated insights and data from Google/Serper. The app features a modern Vue.js frontend and a Django backend with AI integration. Note, no database included as this would be an addon to an existing system.

---

## Project Structure

```
project-root/
├── backend/                    # Django backend (API, business logic, AI integration)
│   ├── ai/                     # AI assistant logic and streaming endpoints
│   │   ├── api/
│   │   └── tests/
│   ├── competitors/            # Competitor data and services
│   │   ├── api/
│   │   └── services/
│   ├── core/                   # Django core settings and entry points
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── profiles/               # Business profile models, services, and utilities
│   │   ├── api/
│   │   ├── mockdata/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── venv/                   # Python virtual environment (not versioned)
│   ├── db.sqlite3              # SQLite DB (if used)
│   ├── manage.py
│   ├── requirements.txt
│   └── ...
├── frontend/                   # Vue.js frontend (UI, components)
│   ├── src/
│   │   ├── App.vue
│   │   └── features/
│   │       └── businessProfileAssistant/
│   │           ├── api/
│   │           └── composables/
│   │           └── components/
│   │           └── tests/                  # Unit and integration tests for businessProfileAssistant feature
│   ├── tests/                  # General frontend tests
│   ├── package.json
│   ├── vue.config.cjs
│   └── ...
└── README.md                   # This file
```


---



## Features

- **AI Business Profile Assistant:**
  Modern chat-based assistant for business owners. Streams AI responses in real time using OpenAI’s GPT-4o. Handles all business-related queries, including profile analysis, competitor comparisons, content generation, actionable suggestions, “what if” scenarios, and so on—all through a single conversational interface. Always starts with a friendly welcome and prompt suggestions.

- **Unified Chat Interface:**
  All insights, analysis, and advice—including competitor information—are delivered through one seamless chat experience. No need to switch between different tools or dashboards.

- **Profile Analysis & Gamification:**
  Analyzes your business profile for completeness, reviews, photos, and local trends. Includes a gamification system with badges and engagement scores to encourage profile improvements.

- **Streaming Architecture:**
  Backend uses Django + Gunicorn for robust streaming support. The `/api/ai/profile-assistant/` endpoint streams incremental AI responses, which are rendered in real time in the frontend chat.

- **Modern Frontend:**
  Built with Vue 3 and modular composables/components. Features a responsive UI, markdown rendering for AI output, and safe handling of user/AI content.

- **No Database Required:**
  The MVP uses mock data and is designed as an addon to existing systems. No database setup is required for core features.

---

## How to Run (Updated for Gunicorn & Streaming)

### Prerequisites

- Python 3.8+
- Node.js (v16+ recommended) & npm
- (Optional) [Poetry](https://python-poetry.org/) or `venv` for Python dependency management

---

### 1. Clone the Repository

```bash
git clone https://github.com/0hscar/profile_comparison.git
cd profile_comparison
```

---

### 2. Backend Setup (Django + Gunicorn)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Copy `.env.example` to `.env` and fill in your API keys (OpenAI, Serper, etc).

- (If you implement a database)
  ```bash
  python manage.py migrate
  ```

**Start the backend with Gunicorn:**
```bash
gunicorn core.wsgi:application -b 127.0.0.1:8000
```
- The backend API will be available at `http://localhost:8000`.

---

### 3. Frontend Setup (Vue.js)

```bash
cd frontend
npm install
npm run serve
```
- The app will be available at `http://localhost:8080`.

---

## Usage

- Open your browser and go to `http://localhost:8080`.
- Click **Open Business Profile Tool** to launch the AI assistant panel.
- Start chatting with the AI assistant! You can:
  - Ask for analysis of your business profile (e.g., “What are my strengths?”)
  - Request competitor comparisons (e.g., “How do I compare to nearby restaurants?”)
  - Generate content (e.g., “Write a catchy Instagram caption for my restaurant”)
  - Explore “what if” scenarios (e.g., “What would happen if I added more photos?”)
  - Get actionable suggestions and insights—all through chat.
- The chat starts with a friendly welcome message and example questions.
- Users profile data is mock data, be found at /backend/profiles/mockdata/fake_profile.py .

---

### 5. Troubleshooting

- If you see CORS errors, make sure `django-cors-headers` is installed and configured in `backend/core/settings.py`:
  ```python
  INSTALLED_APPS = [
      # ...,
      'corsheaders',
  ]
  MIDDLEWARE = [
      'corsheaders.middleware.CorsMiddleware',
      # ...,
  ]
  CORS_ALLOWED_ORIGINS = [
      "http://localhost:8080",
  ]
  ```
- If you want to stop Gunicorn, press `Ctrl+C` in the terminal running it.

---

## Running Tests

### Backend (Django)

You can run backend tests using Django’s test runner or pytest.

**With Django:**
```bash
# Run all backend tests
python manage.py test

# Run tests for a specific app (e.g., ai, profiles, competitors)
python manage.py test ai
python manage.py test profiles
python manage.py test competitors
```

**With pytest (if installed):**
```bash
# Run all backend tests
pytest backend/

# Run tests for a specific service or app
pytest backend/profiles/services/tests/
```

> **Note:**
> Make sure your virtual environment is activated before running tests.
> For fish shell users:
> ```
> source venv/bin/activate.fish
> ```

### Frontend (Vue/Jest)

You can run frontend unit and integration tests using npm scripts.

```bash
cd frontend

# Run all frontend tests
npm test
# or
npm run test
```

You can also run a specific test file with:
```bash
npx jest path/to/your/testfile.spec.js
```

---


## What It Contains

- **Backend (Django):**
  - API endpoints for fetching user restaurant, nearby and similar groups.
  - AI integration for generating summaries and insights.
  - Caching for performance.

- **Frontend (Vue.js):**
  - Responsive UI for input, results, and interactive cards.
  - Toggle between nearby and similar restaurants.
  - Expandable/collapsible restaurant cards.
  - Loading animations and error handling.

---

## Development Notes

- You need valid API keys for OpenAI and Serper in your backend `.env` file.

---

# Version History

## Ver0.3

### Scope:
- **AI-powered business profile**.
  - Modern Chat style Assistant. CHECK
  - Interaction through a single input field. CHECK
  - Streaming responses. CHECK
- **Profile Analysis**.
  - Ask AI assistant to analyze your business profile, such as: CHECK
    - "What are my strengths?"
    - "What are my weaknesses?"
    - "How can I improve my profile?"
    - Profile completeness.
    - And more.
- **Competitor Insights**.
  - User request for competitor insights and comparison. CHECK
  - Either directly compare against nearby or similar from a seperate list. CHECK
  - Direclty ask AI assistant for insights on competitors. CHECK
  - AI Assistant can make suggestions / summarize based on competitor data. CHECK
- **Actionable Insights**.
  - AI assistant can provide actionable insights based on the analysis of your profile and competitors. CHECK
  - For example:
    - "To improve your profile, consider adding more photos."
    - "Your competitors have more reviews, consider encouraging customers to leave feedback."
- **Content Generation**. (Only text for now as stuff such as images are not included in the MVP). CHECK
  - Social media post captions. CHECK
  - Responses to reviews. CHECK
  - Promotional messages. CHECK
- **What if scenarios**. CHECK
  - AI assistant can generate "what if" scenarios based on user input.
- **Welcome & Guidance**.
  - The chat starts with a friendly welcome message and example questions for new users, It's AI = The sky's the limit.

### Out of Scope:
- **Database**: This is designed as an addon to an existing system, no database included.
- **Web Scraping**: Not included in the MVP, but can be added later for more data sources. (browse.ai recommended. MIGHT BE ADDED IF TIME ALLOWS)
- **Charts & Images**: Not included in the MVP, but can be added later for visualizing data - AI generated.
- **No seperate "AI suggestions", "what if", "Profile assistant" etc.**: All of these are now handled by a single chat assistant.
- **Social media integration**: Not included in the MVP, but can be added later for posting content directly to social media platforms.


### Future Improvements / Features:
- **Context injection for AI**
  - Inject user profile data, competitor data, and other relevant information into the AI prompt for more accurate responses.
- **Continously updating Gamification system**.
- **Automatic AI made changes**.
- **Social media integration** Includes AI generated posts from scratch and more.


### User Experience:
- User opens the app and have a slideout profile including AI assistant, nearby and similar restaurants.
- The main content is the AI assistant chat interface.
- User can ask questions, request insights, or compare their profile with nearby/similar restaurants.
- The user gets a quick access AI assistant that can handle various tasks related to their business profile (AI handled changes as future feature)
- Track badges / achievements for completed tasks, such as profile analysis, competitor insights, and content generation, profile improvements, etc.



### TODO:
- **Full tests**
- **Bug fixes**: Address known issues:
  - AI answers adding stuff like "CustomersNone" or Feel free to use this as "isNone" in the response.
- **Features**:
- **Cleanup**: Codebase cleaning, remove unused files and comments. A MUST.
  - **README updates**: "What it contains" has old information
- **Finalize restructuring**: Ensure the project structure is clean and logical.
- **Quality of life improvements**:
  - **UI improvements**: Try to remove excess scrolling.


### TODO - Done
- **Bugs fixed**:
  - Input field stopped rezising after a few lines.
  - Streaming responses
- **Features**:
  - Instant compare from competitor list
  - Toggle between nearby and similar lists
  - AI model selection, OpenAI only for now
- **Quality of life improvements**:
  - **AI response formatting**
  - Enter to send to AI, Shift + Enter to add a new line


### WORKING TESTED STREAMING RESPONSE WITH CURL. EDIT: Streaming responses fully functional now.
curl -N -X POST -H "Content-Type: application/json" -d '{"question": "testing streaming responses"}' http://localhost:8000/api/ai/profile-assistant/



# OLD BELOW
## Ver0.2 OLD ALREADY
### TODO:
- **Streaming responses to the frontend**
- **Change AI Suggestions, Assistant etc etc to a singular chat assistant that does both.**

## Still to do. OLD VERSION

- **Testing:** Add full unit tests for both backend and frontend components, edge cases and error handling. No more 404 errors caused by empty variables.
- **bug fixes:** Address any known issues or bugs. Known bugs include:
  - Double API call on direct compare from nearby/similar list.
  - If input searched a second time, competitor query get's wild and ignores location/address
  - Some UI elements overlap.
- **Mandatory Features:** AI response formating.
- **Mandatory Cleanup:** Codebase cleaning

## Fixed bugs. OLD VERSION

- **Nearby restaurants bug**

## Performance fixes

- **Changed to response.parse:** Faster OpenAI responses

## Future features: OLD VERSION

- **Improvements:** More data soures, Improved UI/UX based on customers requests / self noticed possibilities, Focused data driven / Casual data driven suggestions.
- **Streaming AI Response**
- **Potential REST Framework**
- **Web Scraping**: Image size checks, Menu and Open hours, Online reservation
- **Instead of Web Scraping**: browse.ai . Does the scraping for you
- **Charts:** Either AI generated or coded.
- **Country Codes:** Mapping country codes "fi": "Finland",

### Not visible for user OLD VERSION

- **Double API call on direct compare via nearby / similar list**
- **After change to response.parse -> location / address gets ignored on OpenAI call. CRUCIAL FIX BEFORE LAUNCH**

## Scope. OLD VERSION

- Serper API (Google) + AI (GPT 4.1-mini) generated suggestions, comparison and extra insights
- Either choose from a list of nearby / similar restaurant. Or Search for multiple by name or "thai food". Direct search also available. Simple UI implemented to achieve this
- Designed as a slap-on slide-in feature for an existing Vue app
- response.parse OpenAI call used for faster response times and structured returns
-- Caching prompts, responses and fetched data from Serper API.
-- Feeds changeable data last into the AI prompt as OpenAI auto caches and it redoes it when it finds changed data.

## Fixed and passed tests. OLD VERSION

- Results.spec.js
- ComparatorSlideout.spec.js
- InputForm.spec.js
- RestaurantCard.spec.js
- SidebarRestaurantList.spec.js

## Explain. OLD VERSION
- temperature. the lesser number minimized changeability in repsonses. Less varying answers, can be experimented with
- csrf_exempt protects from unauthorized third party sites.

## Left out. OLD VERSION
- Chart generation/ visualization. -> future
- Preview improvements using the AI generated content. --> Is a future feature in my mind, doesn't fit in a MVP
- Web Scraping --> A massive improvement as LLMs based on limited data can get things wrong -> browse.ai recommended
- Running modern local models if infrastructure can support it.
-
