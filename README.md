# Practice Hub

## Overview

The practice hub is a dashboard that can be used to track practicing an instrument and set goals to progress toward. I'm a musician and wanted something that I could use to easily track when I played and eventually see different insights on that practice. I felt like this was a great project to add to my portfolio to show off some of my architecture skills and different technologies I know how to use.

## Live Demo

🔗 **[Will be live soon](https://kuhrt.codes)**

## Skills Demonstrated

This project showcases the following technical skills and concepts:

- **Full-stack Architecture**: Shows I can archetect a full-stack application. I'm using Python, Typescript, Postgres and Keycloak.
- **Front-end Data Organization**: A dashboard with data-driven elements (charts, tables, etc) that's easy to use and nice to look at
- **API Structure and Ingestion**: I like API-driven architecture for its versatility and extensibility. This shows general preferences for structuring and ingesting an API
- **Database Schema Management**: Quick look into how I like to handle models and their schemas
- **Caching through Redis**: Using Redis to cache outside API data (from Spotify)
- **Authentication/Authorization**: Using JWT flows to gain access to data

## Technology Stack

### Core Technologies

- **Next.js (Typescript)**: For React projects, Next.js is my favorite choice. There are a lot of haters online, so below I've listed why I like it and address most concerns I see about it.
  - It's very opinionated. I tend to work with all levels of developers from all around the globe. Its opinionated approach makes patterns and documentation easy to find/follow and are readily available.
  - Use what you need and ignore the rest. If I create a React Router project or pure React project, I always end up building what Next has out of the box. People argue that Next is bloated, but you don't have to use what you don't want to. It can be light as a feather, this project being an example of that.
  - It's the standard, even across Vue and Angular projects. When React comes out with a new feature, Next has it implemented first. Its patterns and features are also followed closely and copied by frameworks like Nuxt and Angular.
  - With the introduction of Turbopack, development is no longer slow or lags with hot-reloading. I'll admit, Vite still probably has it beat, but it's hardly noticeable.
  - It can be deployed anywhere. No, you're not stuck with Vercel. I've deployed Next.js projects to containers (Docker, Kubernetes, and more), stand-alone servers, in .NET projects, AWS, Azure, and yes, Vercel. For example, this project is deployed to a Digital Ocean droplet running multiple Docker images and serving this site.
  - It is not just for SSR and SEO. I see this a lot for some reason being an argument against using Next. Yes, it has these features out of the box, but you don't have to use either. Also, this should not be the only reasons you're choosing a stack for a web application or site.
  - I don't hate other libraries/frameworks/approaches at all. I prototype all the time with Vite, React Router, and even Astro. These and more are all great solutions, however, I'm wanting to show my go to for enterprise solutions
- **Fast API (Python)**: I don't have quite the experience in different choices in building an API with Python other than Flask. I like FastAPI way more and feel like it's a strong candidate for building an API in Python.
- **Pydantic/SQLModel/SQLAlchemy (Postgres)**: To interact with my Postgres db, I'm using these libraries to organize and validate my data.
- **Keycloak (auth)**: Open-source, easy to use, and production ready. I haven't found a use-case that Keycloak can't cover.
- **Redis**: Who doesn't love Redis? Hands down makes your apps faster and not too difficult to implement. I will use Redis for caching on any project I can.
- **Tanstack**: The project uses Tanstack's query and data tables. I love the state management Tanstack provides. It's hard to beat in my mind.
- **Pytest**: Python testing
- **Jest**: Classic for unit/integration tests
- **Cypress**: I like Cypress over Playwright as just a personal preference. Excellent component and E2E testing
- **Docker**: The `.tools` contains a compose file to run the project locally. I also have versions of this for the live demo.

### Additional Tools & Libraries

- **uv**: I love this package for Python. I generally use it exclusively when creating new Python projects. It's so little work to create organized, sharable projects.
- **Shadcn/ui**: Amazing Tailwind UI kit to help build great looking, usable dashboards fast
- **Alembic**: Migrations can be tricky, and Alembic is an incredibly helpful tool
- **Auth.js**: Incredibly fast Auth library. Best option that I'm aware of as long as a completely custom solution is needed.
- **Zustand**: For seamless state management for any cases Tanstack can't cover. Much cleaner and easier to use than Redux.
- **React Hook Form**: I love the hooks and structure this library gives. Handles any form case imaginable.
- **Zod**: Every form needs validation. Zod provides straight-forward, structured validations

## Local Development Setup

### Prerequisites

Before running this project locally, ensure you have the following installed:

- **NPM**: [Download](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
  - Package manager
  - Latest version recommended
- **uv**: [Install](https://docs.astral.sh/uv/getting-started/installation/)
- **Docker**: [Install](https://docs.docker.com/desktop/)

### Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Kuhrt/portfolio-practice-hub.git
   cd portfolio-practice-hub
   ```

2. **Create and run containers**

   ```bash
   cd .tools
   docker compose up
   ```

3. **Setup Keycloak**

   1. A realm and client will need to be created
   2. Ensure all needed flows for JWT are enabled for the created client
   3. Create your test user

4. **Install API dependencies**

   ```bash
   cd api
   uv sync
   ```

5. **Install Web App dependencies**

   ```bash
   cd web
   npm i
   ```

6. **Environment Configuration**

   ```bash
   # Copy environment template in the api/ and web/ directories
   cp .env .env.local

   # Edit .env file with your configuration
   # Ensure all values are populated
   ```

7. **Database Setup**

   ```bash
   cd api
   uv run alembic upgrade head
   ```

8. **Start the development server**

   The easiest way is using the VS Code "Run and Debug" feature. There is a `launch.json` file already included with the commands needed.

9. **Access the application**

   - Web Application: Open your browser and navigate to: `http://localhost:3000`
   - API Swagger: Open your browser and navigate to: `http://localhost:8000/docs`

## Project Structure

```
portfolio-practice-hub/
├── .tools/
│   └── docker-compose.yml
├── api/
├── web/
└── README.md
```

## Repository Information

- **Status**: In Development
- **Type**: Full-stack portfolio project
- **Contributions**: This repository does not accept contributions as it's designed to showcase individual technical skills

---

_This project was created by Kuhrt as part of my software development portfolio._
