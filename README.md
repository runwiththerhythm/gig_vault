# [Gig_Vault](https://gig-vault-2fe6800a7bea.herokuapp.com)

Developer: ([runwiththerhythm](https://www.github.com/runwiththerhythm))

[![GitHub commit activity](https://img.shields.io/github/commit-activity/t/runwiththerhythm/gig_vault)](https://www.github.com/runwiththerhythm/gig_vault/commits/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/runwiththerhythm/gig_vault)](https://www.github.com/runwiththerhythm/gig_vault/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/runwiththerhythm/gig_vault)](https://www.github.com/runwiththerhythm/gig_vault)
[![badge](https://img.shields.io/badge/deployment-Heroku-purple)](https://gig-vault-2fe6800a7bea.herokuapp.com)

## Introduction

Gig Vault is a personal live music diary application that helps fans track, organise, and remember their concert experiences. Users can log gigs with band lineups, venues, dates, photos, and videos and create an archive of their concert journey. Unlike generic apps, Gig Vault is designed specifically for concerts and festivals, making it easier to preserve memories and reflect on the role of live music in personal culture.

Designed to appeal to festival goers who want to remember all the bands they've seen when and where over the years.

**Site Mockup**
![screenshot](documentation/mockup.png)

source: [gig_vault amiresponsive](https://ui.dev/amiresponsive?url=https://gig-vault-2fe6800a7bea.herokuapp.com)

## UX

### The 5 Planes of UX

#### 1. Strategy

**Purpose**
- Provide music fans with a dedicated tool to log, organize, and relive their live music experiences.
- Offer users an intuitive platform to browse their personal gig history, including bands, venues, images, and media links.
- Support users with features like statistics, reminders, and media integration to make their gig history engaging and meaningful.

**Primary User Needs**
- Users need a simple way to record new gigs (band, venue, date, notes, images, videos).
- Users need the ability to browse past gigs quickly, either by date, band, or venue.
- Users need a secure, private space where their data and memories are preserved.
- Users want to see patterns and highlights (e.g, most seen bands, attended festivals, anniversary reminders).

**Business Goals**
- Deliver a unique niche platform focusing specifically on live music memories
- Encourage long-term engagement by giving users reasons to revisit (e.g., stats, reminders, multimedia playback).
- Demonstrate a well-structured, user-centered Django web application for academic and portfolio purposes.

#### 2. Scope

**[Features](#features)** (see below)

**Content Requirements**
- Gig management (create, update, delete).
- Band management (headliners and support artists).
- Venue management (integrated with Mapbox Search JS).
- Image upload and cover image selection (via Cloudinary).
- YouTube video linking and auto-search.
- Stats and insights (total gigs, most-seen band, “On This Day”).
- User authentication (signup, login, logout).
- Dashboard view with upcoming and attended gigs.
- Error handling pages (e.g., 404, 500).

#### 3. Structure

**Information Architecture**
- **Navigation Menu**:
  - Links to Home, Dashboard, My Gigs, Add Gig, Logout..
- **Hierarchy**:
  - Dashboard and “My Gigs” provide a clear overview of past and upcoming gigs.
  - Gig detail pages highlight band, venue, and media.
  - Create/Edit forms use autocomplete for bands/venues, with clear CTAs for “add new”.

**User Flow**
1. Guest user visits Landing Page → learns about Gig Vault, sees a call-to-action to sign up or log in.
2. User signs up or logs in → gains access to Dashboard and gig tools.
3. User creates a gig entry → fills band, venue, date, adds images/videos.
4. User browses past gigs or adds new ones over time → personal archive grows into a complete music history.
5. User explores stats → checks most-seen bands etc.

#### 4. Skeleton

**[Wireframes](#wireframes)** (see below)

#### 5. Surface

**Visual Design Elements**
- **[Colours](#colour-scheme)** (see below)
- **[Typography](#typography)** (see below)

### Colour Scheme

I used [coolors.co](https://coolors.co) to finalise my color palette.

![screenshot](documentation/coolors.png)

The Gig Vault palette was chosen to reflect the energy and atmosphere of live music, especially the lighting set you experience at concerts and festivals.

Fiery Orange (#FF4C1A) & Golden Yellow (#FFDD33)
Inspired by stage lights, pyrotechnics, and sunset skies at outdoor gigs. These warm tones bring immediacy and excitement to buttons and call-to-action elements.

Electric Purple (#8E4CD9) & Magenta Pink (#C2188D)
Drawn from the neon floods, strobes and lasers. These cooler, high-energy colours balance the warm tones and give a sense of atmosphere and nightlife.

Light Mode Foundations (#FAF9F6 background, #1A1A1A text)
Chosen for readability and a clean diary-like feel, so users can comfortably browse and log gigs in daylight settings.

Dark Mode Foundations (#1E1229 deep purple background, #F5F3FA text)
Inspired by the low-light conditions of concert venues, with a subtle purple tint to feel immersive but easy on the eyes. This mode echoes the ambience of being in the crowd under stage lighting.

By combining these brights with neutral light and dark foundations, Gig Vault maintains accessibility (AA contrast) while also capturing the vibrant, high-contrast lighting environment of live shows.

### Typography

- [Modern Thrash](https://thebrandedquotes.sellfy.store/p/modern-thrash-font/) was used for the primary headers and titles. This font evokes heavy metal artwork, festival branding and live posters, with sharp edges and a distorted aesthetic that ties directly into the live music scene and the energy it creates.
- System ui font has been used for the body to keep it readable and clear on all devices. 

## Wireframes

![screenshot](documentation/wireframes.png) |

## User Stories

| Target | Expectation | Outcome |
| --- | --- | --- |
| As a first time visitor,|  I can view detailed information about the app without having to register, | so that I can decide if I want to use it. |
| As a first time visitor, | I would like to be able to navigate the site easily | so that I can find relevant information quickly. |
| As a new user | I can sign up easily using a registration form | so that I can create an account and start using the app. |
| As a registered user | I can log in securely | so that I can access my private dashboard and saved gigs.|
| As a user who forgot my password | I can reset it via email | so that I can regain access to my account.
| As a logged in user,| I can log out, | so that I can end my session securely.|
| As a user,| I can view a friendly error page if I hit a dead link | so that I’m not confused or lost. |
| As a logged in user,| I want to add a gig I attended | so that I can manage user engagement effectively. |
| As a logged in user, | I want the band field to autocomplete when typing| so I don’t create duplicate entries. |
| As a logged in user, | I want to view the full details of a specific gig, | so I can revisit memories and see all the information I entered.|
| As a logged in user, | I want to edit an existing gig,  | so I can fix mistakes or update information like venue, date, or notes.|
| As a logged in user, |  I want to delete a gig, | so I can remove any accidental or unwanted entries.|
| As a logged in user, | I want to view a list of all gigs I’ve entered,| so I can browse my gig history easily.|
| As a logged in user, | I want to upload and manage images for a gig,| so I can visually document the concert experience.|
| As a logged in user, |I want to record a festival as a gig that contains multiple band performances, | so I can document the full experience in one place.|
| As a logged in user, | I want to add other artists who performed at the same gig,  | sso I can log the full lineup. |
| As a logged in user,| I want to see relevant YouTube videos from a gig,| so I can relive the performance without having to manually search. |
| As a logged in user, | I want to quickly see the setlist from the gig,| so I can remember what songs were played. |

## Features

### Existing Features

| Feature | Notes | Screenshot |
| --- | --- | --- |
| Register / Login / Logout | Handled by django-allauth, allowing users to create secure accounts, log in, and log out. | ![screenshot](documentation/features/register.png) |
| Dashboard | The central hub showing upcoming gigs, attended gigs, and quick stats. | ![screenshot](documentation/features/dashboard.png) |
| My Gigs | Full list view of all a user’s gigs with filtering for upcoming vs past gigs. Entries are displayed as cards with cover images and details. | ![screenshot](documentation/features/my-gigs.png) |
|Add Gig | Users can log a gig they attended or are planning to attend. The form supports band autocomplete, venue search (Mapbox), gig date, status, and genre.| ![screenshot](documentation/features/add-new-gig1.png) |
| Edit / Delete Gig | Existing gig entries can be updated or removed, giving users full control over their vault. | ![screenshot](documentation/features/edit-gig1.png) |
| Band Autocomplete | Powered by django-autocomplete-light, users can quickly search and select existing bands or add new ones via modal. | ![screenshot](documentation/features/band-autocomplete.png) |
| Venue Search | Uses Mapbox Search JS to autocomplete venue details. Venue name, city, and country are stored without needing coordinates. | ![screenshot](documentation/features/venue.png) |
| Image Uploads | Users can upload multiple gig images (via Cloudinary). One image can be marked as the cover, and previews are shown before saving. | ![screenshot](documentation/features/image-uploads.png) |
| YouTube Integration | Users can auto-search YouTube for videos of their gig and link them directly into the entry. | ![screenshot](documentation/features/youtube.png) |
| About Page | Introduces the Gig Vault project and its purpose.| ![screenshot](documentation/features/about.png) |
| 404 | The 404 error page will indicate when a user has navigated to a page that doesn't exist, replacing the default Heroku 404 page with one that ties into the site's look and feel. | ![screenshot](documentation/features/404.png) |
| Messages / Feedback | Django messages framework provides clear feedback for actions (e.g., gig created, updated, deleted). | ![screenshot](documentation/features/404.png) |
| Heroku Deployment | Fully deployed to Heroku with Postgres, Cloudinary, and Whitenoise. | ![screenshot](documentation/features/404.png) |

### Future Features

- **Festival Child Gigs**: Ability to create a “parent” festival entry that contains multiple band performances as child gigs. Helps users track festival weekends in detail.
- **Social Sharing**: Quick-share options for individual gig entries to platforms like Instagram, Facebook, and X (Twitter). Lets users show off their vault highlights.
- **Dark Mode Toggle**:A built-in dark theme for night-time browsing, fitting the live music aesthetic and reducing eye strain.
- **Advanced Stats**: A calendar-based view for upcoming gigs, making it easier to see what’s coming up at a glance.
- **Calendar View**: Enable users to reply to comments, creating nested comment threads for better discussions.
- **Notifications / Reminders**: Email or dashboard notifications reminding users about upcoming gigs or anniversaries of past ones.
- **Export / Import**: IAbility to export a user’s gig history to CSV/JSON or import past gig data from external services.
- **Email Subscriptions**: Allow users to subscribe to receive email notifications for new features, updates, and newsletter.
- **Analytics**: For better understanding of how the user uses the site to better future improvements.
- **Multilingual Support**: Add the ability to write and view in multiple languages, broadening the audience.
- **Mobile PWA**: Progressive Web App mode for offline access and quick “Add to Home Screen” installs on iOS/Android.
- **SEO Optimization**: Implement features for SEO, such as meta tags, custom URLs, and keywords for better search engine ranking.
- **Custom Themes for Users**: Allow users to customize the visual theme of the site (colors, fonts, etc.) to suit their preferences.

## Tools & Technologies

| Tool / Tech | Use |
| --- | --- |
| [![badge](https://img.shields.io/badge/Markdown_Builder-grey?logo=markdown&logoColor=000000)](https://markdown.2bn.dev) | Generate README and TESTING templates. |
| [![badge](https://img.shields.io/badge/Git-grey?logo=git&logoColor=F05032)](https://git-scm.com) | Version control. (`git add`, `git commit`, `git push`) |
| [![badge](https://img.shields.io/badge/GitHub-grey?logo=github&logoColor=181717)](https://github.com) | Secure online code storage. |
| [![badge](https://img.shields.io/badge/HTML-grey?logo=html5&logoColor=E34F26)](https://en.wikipedia.org/wiki/HTML) | Main site content and layout. |
| [![badge](https://img.shields.io/badge/CSS-grey?logo=css&logoColor=1572B6)](https://en.wikipedia.org/wiki/CSS) | Design and layout. |
| [![badge](https://img.shields.io/badge/JavaScript-grey?logo=javascript&logoColor=F7DF1E)](https://www.javascript.com) | User interaction on the site. |
| [![badge](https://img.shields.io/badge/jQuery-grey?logo=jquery&logoColor=0769AD)](https://jquery.com) | User interaction on the site. |
| [![badge](https://img.shields.io/badge/Python-grey?logo=python&logoColor=3776AB)](https://www.python.org) | Back-end programming language. |
| [![badge](https://img.shields.io/badge/Heroku-grey?logo=heroku&logoColor=430098)](https://www.heroku.com) | Hosting the deployed back-end site. |
| [![badge](https://img.shields.io/badge/Bootstrap-grey?logo=bootstrap&logoColor=7952B3)](https://getbootstrap.com) | Front-end CSS framework for modern responsiveness and pre-built components. |
| [![badge](https://img.shields.io/badge/Django-grey?logo=django&logoColor=092E20)](https://www.djangoproject.com) | Python framework for the site. |
| [![badge](https://img.shields.io/badge/PostgreSQL-grey?logo=postgresql&logoColor=4169E1)](https://www.postgresql.org) | Relational database management. |
| [![badge](https://img.shields.io/badge/Cloudinary-grey?logo=cloudinary&logoColor=3448C5)](https://cloudinary.com) | Online static file storage. |
| [![badge](https://img.shields.io/badge/WhiteNoise-grey?logo=python&logoColor=FFFFFF)](https://whitenoise.readthedocs.io) | Serving static files with Heroku. |
| [![badge](https://img.shields.io/badge/Canva-grey?logo=canva&logoColor=00C4CC)](https://www.canva.com/p/canvawireframes) | Creating wireframes. |
| [![badge](https://img.shields.io/badge/Font_Awesome-grey?logo=fontawesome&logoColor=528DD7)](https://fontawesome.com) | Icons. |
| [![badge](https://img.shields.io/badge/ChatGPT-grey?logo=openai&logoColor=75A99C)](https://chat.openai.com) | Help debug, troubleshoot, research, code logic and pair program. |

## Database Design

### Data Model

Gig Vault uses a relational schema built in PostgreSQL with models representing users, gigs, bands, venues, images, videos and genres.

![screenshot](documentation/erd.png)

 [`Mermaid flowchart`](https://mermaid.live). 
I have used `Mermaid` to generate an ERD of my project.

erDiagram
    direction TB
    User {
        int id PK
        string username
        string email
    }

    Band {
        int id PK
        string name
    }

    Venue {
        int id PK
        string venue_name
        string venue_city
        string venue_country
        string address_text "optional"
    }

    Genre {
        int id PK
        string name
    }

    GigImage {
        int id PK
        string image "Cloudinary"
        string caption "optional"
        boolean is_cover "max one per gig"
        int gig_id FK
    }

    GigVideo {
        int id PK
        string url
        datetime added_at
        int gig_id FK
        int added_by_id FK "nullable → User"
    }

    Gig {
        int id PK
        date date
        boolean is_festival
        string tour_title
        string status "upcoming / attended"
        text notes "rich text (Summernote)"
        int user_id FK
        int band_id FK "headliner"
        int venue_id FK
    }

    User ||--o{ Gig : "owns"
    Band ||--o{ Gig : "headliner"
    Venue ||--o{ Gig : "hosted at"
    Gig }o--o{ Band : "other_artists (supports)"
    Genre ||--o{ Gig : "genres"
    Gig ||--o{ GigImage : "images"
    Gig ||--o{ GigVideo : "videos"
    User ||--o{ GigVideo : "added_by (optional)"

source: [Mermaid](https://www.mermaidchart.com/app/projects/9d020117-8aa3-4abc-879e-0ce435a4ec55/diagrams/74682d3b-637b-42e9-ae1d-65b4f302a37f/version/v0.1/edit)

## Agile Development Process

### GitHub Projects

[GitHub Projects](https://www.github.com/runwiththerhythm/gig_vault/projects) served as an Agile management tool for this project. Through it, User Stories, issues/bugs and tasks were planned, then subsequently tracked on a regular basis using the Kanban project board.

![screenshot](documentation/gh-projects.png)

### GitHub Issues

[GitHub Issues](https://www.github.com/runwiththerhythm/gig_vault/issues) served as an another Agile tool. There, I managed my User Stories and Milestone tasks and tracked any issues/bugs.

| Link | Screenshot |
| --- | --- |
| [![GitHub issues](https://img.shields.io/github/issues/runwiththerhythm/gig_vault)](https://www.github.com/runwiththerhythm/gig_vault/issues) | ![screenshot](documentation/gh-issues-open.png) |
| [![GitHub closed issues](https://img.shields.io/github/issues-closed/runwiththerhythm/gig_vault)](https://www.github.com/runwiththerhythm/gig_vault/issues?q=is%3Aissue+is%3Aclosed) | ![screenshot](documentation/gh-issues-closed.png) |

## Testing

> [!NOTE]  
> For all testing, please refer to the [TESTING.md](TESTING.md) file.

## Deployment

The live deployed application can be found deployed on [Heroku](https://gig-vault-2fe6800a7bea.herokuapp.com).

### Heroku Deployment

This project uses [Heroku](https://www.heroku.com), a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

Deployment steps are as follows, after account setup:

- Select **New** in the top-right corner of your Heroku Dashboard, and select **Create new app** from the dropdown menu.
- Your app name must be unique, and then choose a region closest to you (EU or USA), then finally, click **Create App**.
- From the new app **Settings**, click **Reveal Config Vars**, and set your environment variables to match your private `env.py` file.

> [!IMPORTANT]  
> This is a sample only; you would replace the values with your own if cloning/forking my repository.

| Key | Value |
| --- | --- |
| `CLOUDINARY_URL` | user-inserts-own-cloudinary-url |
| `DATABASE_URL` | user-inserts-own-postgres-database-url |
| `DISABLE_COLLECTSTATIC` | 1 (*this is temporary, and can be removed for the final deployment*) |
| `SECRET_KEY` | any-random-secret-key |

Heroku needs some additional files in order to deploy properly.

- [requirements.txt](requirements.txt)
- [Procfile](Procfile)
- [.python-version](.python-version)

You can install this project's **[requirements.txt](requirements.txt)** (*where applicable*) using:

- `pip3 install -r requirements.txt`

If you have your own packages that have been installed, then the requirements file needs updated using:

- `pip3 freeze --local > requirements.txt`

The **[Procfile](Procfile)** can be created with the following command:

- `echo web: gunicorn app_name.wsgi > Procfile`
- *replace `app_name` with the name of your primary Django app name; the folder where `settings.py` is located*

The **[.python-version](.python-version)** file tells Heroku the specific version of Python to use when running your application.

- `3.12` (or similar)

For Heroku deployment, follow these steps to connect your own GitHub repository to the newly created app:

Either (*recommended*):

- Select **Automatic Deployment** from the Heroku app.

Or:

- In the Terminal/CLI, connect to Heroku using this command: `heroku login -i`
- Set the remote for Heroku: `heroku git:remote -a app_name` (*replace `app_name` with your app name*)
- After performing the standard Git `add`, `commit`, and `push` to GitHub, you can now type:
	- `git push heroku main`

The project should now be connected and deployed to Heroku!

### Cloudinary API

This project uses the [Cloudinary API](https://cloudinary.com) to store media assets online, due to the fact that Heroku doesn't persist this type of data.

To obtain your own Cloudinary API key, create an account and log in.

- For "Primary Interest", you can choose **Programmable Media for image and video API**.
- *Optional*: edit your assigned cloud name to something more memorable.
- On your Cloudinary Dashboard, you can copy your **API Environment Variable**.
- Be sure to remove the leading `CLOUDINARY_URL=` as part of the API **value**; this is the **key**.
    - `cloudinary://123456789012345:AbCdEfGhIjKlMnOpQrStuVwXyZa@1a2b3c4d5)`
- This will go into your own `env.py` file, and Heroku Config Vars, using the **key** of `CLOUDINARY_URL`.

### PostgreSQL

This project uses a [Code Institute PostgreSQL Database](https://dbs.ci-dbs.net) for the Relational Database with Django.

> [!CAUTION]
> - PostgreSQL databases by Code Institute are only available to CI Students.
> - You must acquire your own PostgreSQL database through some other method if you plan to clone/fork this repository.
> - Code Institute students are allowed a maximum of 8 databases.
> - Databases are subject to deletion after 18 months.

To obtain my own Postgres Database from Code Institute, I followed these steps:

- Submitted my email address to the CI PostgreSQL Database link above.
- An email was sent to me with my new Postgres Database.
- The Database connection string will resemble something like this:
    - `postgres://<db_username>:<db_password>@<db_host_url>/<db_name>`
- You can use the above URL with Django; simply paste it into your `env.py` file and Heroku Config Vars as `DATABASE_URL`.

### WhiteNoise

This project uses the [WhiteNoise](https://whitenoise.readthedocs.io/en/latest/) to aid with static files temporarily hosted on the live Heroku site.

To include WhiteNoise in your own projects:

- Install the latest WhiteNoise package:
    - `pip install whitenoise`
- Update the `requirements.txt` file with the newly installed package:
    - `pip freeze --local > requirements.txt`
- Edit your `settings.py` file and add WhiteNoise to the `MIDDLEWARE` list, above all other middleware (apart from Django’s "SecurityMiddleware"):

```python
# settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # any additional middleware
]
```


### Local Development

This project can be cloned or forked in order to make a local copy on your own system.

For either method, you will need to install any applicable packages found within the [requirements.txt](requirements.txt) file.

- `pip3 install -r requirements.txt`.

You will need to create a new file called `env.py` at the root-level, and include the same environment variables listed above from the Heroku deployment steps.

> [!IMPORTANT]  
> This is a sample only; you would replace the values with your own if cloning/forking my repository.

Sample `env.py` file:

```python
import os

os.environ.setdefault("SECRET_KEY", "any-random-secret-key")
os.environ.setdefault("DATABASE_URL", "user-inserts-own-postgres-database-url")
os.environ.setdefault("CLOUDINARY_URL", "user-inserts-own-cloudinary-url")  # only if using Cloudinary

# local environment only (do not include these in production/deployment!)
os.environ.setdefault("DEBUG", "True")
```

Once the project is cloned or forked, in order to run it locally, you'll need to follow these steps:

- Start the Django app: `python3 manage.py runserver`
- Stop the app once it's loaded: `CTRL+C` (*Windows/Linux*) or `⌘+C` (*Mac*)
- Make any necessary migrations: `python3 manage.py makemigrations --dry-run` then `python3 manage.py makemigrations`
- Migrate the data to the database: `python3 manage.py migrate --plan` then `python3 manage.py migrate`
- Create a superuser: `python3 manage.py createsuperuser`
- Load fixtures (*if applicable*): `python3 manage.py loaddata file-name.json` (*repeat for each file*)
- Everything should be ready now, so run the Django app again: `python3 manage.py runserver`

If you'd like to backup your database models, use the following command for each model you'd like to create a fixture for:

- `python3 manage.py dumpdata your-model > your-model.json`
- *repeat this action for each model you wish to backup*
- **NOTE**: You should never make a backup of the default *admin* or *users* data with confidential information.

#### Cloning

You can clone the repository by following these steps:

1. Go to the [GitHub repository](https://www.github.com/runwiththerhythm/gig_vault).
2. Locate and click on the green "Code" button at the very top, above the commits and files.
3. Select whether you prefer to clone using "HTTPS", "SSH", or "GitHub CLI", and click the "copy" button to copy the URL to your clipboard.
4. Open "Git Bash" or "Terminal".
5. Change the current working directory to the location where you want the cloned directory.
6. In your IDE Terminal, type the following command to clone the repository:
	- `git clone https://www.github.com/runwiththerhythm/gig_vault.git`
7. Press "Enter" to create your local clone.

#### Forking

By forking the GitHub Repository, you make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original owner's repository. You can fork this repository by using the following steps:

1. Log in to GitHub and locate the [GitHub Repository](https://www.github.com/runwiththerhythm/gig_vault).
2. At the top of the Repository, just below the "Settings" button on the menu, locate and click the "Fork" Button.
3. Once clicked, you should now have a copy of the original repository in your own GitHub account!

### Local VS Deployment

There are no remaining major differences between the local version when compared to the deployed version online.

## Credits

### Content

| Source | Notes |
| --- | --- |
| [Markdown Builder](https://markdown.2bn.dev) | Help generating Markdown files |
| [I Think Therefore I Blog](https://codeinstitute.net) | Code Institute walkthrough project inspiration |
| [Bootstrap](https://getbootstrap.com) | Various components / responsive front-end framework |
| [Cloudinary API](https://cloudinary.com) | Cloud storage for static/media files |
| [Whitenoise](https://whitenoise.readthedocs.io) | Static file service |
| [Python Tutor](https://pythontutor.com) | Additional Python help |
| [ChatGPT](https://chatgpt.com) | Help with code logic and explanations |

### Media

- Images
    - [Pexels](https://www.pexels.com)
    - [Unsplash](https://unsplash.com)

| Source | Notes |
| --- | --- |
| [favicon.io](https://favicon.io) | Generating the favicon |
| [Font Awesome](https://fontawesome.com) | Icons used throughout the site |

### Acknowledgements

- I would like to thank;
The [Code Institute](https://codeinstitute.net) for their learning materials and project assignment.
My Code Institute mentor, [Tim Nelson](https://www.github.com/TravelTimN) and my Nescot college facilitators Johnathan Jacobson and [Komal Karir](https://github.com/Komals-Code4All) for their support throughout development of this project.

