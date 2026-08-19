<div align="center">

# 🎓 CrossSkill

<sub>Peer-to-Peer Student Skill Exchange Platform</sub>

---

### Problem Statement PS-05 — Skill Swap

[![Status](https://img.shields.io/badge/STATUS-IN%20DEVELOPMENT-orange?style=for-the-badge)](#-project-status)
[![React](https://img.shields.io/badge/REACT-FRONTEND-149eca?style=for-the-badge&logo=react&logoColor=white)](#-tech-stack)
[![Python](https://img.shields.io/badge/PYTHON-3.12.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](#-tech-stack)
[![Flask](https://img.shields.io/badge/FLASK-BACKEND-000000?style=for-the-badge&logo=flask&logoColor=white)](#-tech-stack)
[![Neon](https://img.shields.io/badge/NEON-POSTGRESQL-00E599?style=for-the-badge&logo=postgresql&logoColor=white)](#️-database-schema)
[![License](https://img.shields.io/badge/LICENSE-TBD-lightgrey?style=for-the-badge)](#-project-status)

**Repository:** _add repo link here_

</div>

---

## 🌟 About CrossSkills

> CrossSkills is an innovative peer-to-peer knowledge exchange platform bridging learners through mutual value. Users authenticate to access a robust search engine, personalized self-growth dashboards, smart skill-matching algorithms, active collaboration hubs with chat, and dynamic profile management — enabling seamless, zero-cost reciprocal learning.

---

## 📌 Overview

| | |
|---|---|
| **Project Name** | CrossSkill |
| **Problem Statement** | PS-05 — Skill Swap |
| **Category** | Student Collaboration / Skill Matching |
| **Target Users** | Students (beginner → advanced) |
| **Version** | 1.0 |

CrossSkill helps students find peers who can teach them the skills they want to learn — and lets them teach what they already know in return.

> *"I can teach what I know, and I can learn what I don't know."*

---

## 🧩 Problem Statement

Students possess a wide range of technical and non-technical skills, but there is no centralized way for them to discover peers who can teach or learn from one another:

- Students don't know who has a particular skill or what level they're at
- There's no easy way to compare desired skills against another person's acquired skills
- Manual searching offers no intelligent compatibility scoring
- There is no single, integrated flow from **discovery → request → chat → scheduling → feedback**

**Example:** Student A knows Python (Advanced) and wants to learn React. Student B knows React (Advanced) and wants to learn Python. These two are ideal skill-swap partners — but nothing currently connects them.

---

## 🔁 Core Concept

Every profile is built on a two-sided skill relationship:

| Type | Meaning | Example |
|---|---|---|
| **Offered / Acquired Skill** | What the user already knows and can teach | Python — Advanced |
| **Desired / Target Skill** | What the user wants to learn | React — Beginner |

```
User A's Desired Skill  ≈  User B's Offered Skill
User B's Desired Skill  ≈  User A's Offered Skill
```

A **mutual match** (both directions align) produces the strongest recommendation.

---

## ✨ Key Features

<div align="center">

[![Auth](https://img.shields.io/badge/🔐-AUTHENTICATION-1f6feb?style=for-the-badge)]()
[![Profile](https://img.shields.io/badge/👤-PROFILE-1f6feb?style=for-the-badge)]()
[![Search](https://img.shields.io/badge/🔍-SEARCH-1f6feb?style=for-the-badge)]()
[![Recommend](https://img.shields.io/badge/🎯-RECOMMENDATIONS-1f6feb?style=for-the-badge)]()
[![Chat](https://img.shields.io/badge/💬-CHAT-1f6feb?style=for-the-badge)]()
[![Schedule](https://img.shields.io/badge/🗓️-SCHEDULING-1f6feb?style=for-the-badge)]()
[![Feedback](https://img.shields.io/badge/⭐-FEEDBACK-1f6feb?style=for-the-badge)]()

</div>

| Feature | Description |
|---|---|
| **Authentication & Profile** | Secure account creation, hashed-password login, offered/desired skills with proficiency levels |
| **Search** | Search students by name or skill |
| **Recommendation Engine** | Global matching by skill, level, category, and rating — with a computed match score |
| **Connections** | Send, accept, or reject skill-swap requests (`PENDING` → `ACTIVE` → `COMPLETED`) |
| **Chat** | Unlocked once a connection is accepted; messages stored per connection |
| **Scheduling** | Set session start/end time, number of slots, and agenda |
| **Feedback** | 1–5 star rating + written review, contributing to average user rating |

---

## 🗺️ User Flow

```
Landing Page
      ↓
User Login
      ↓
Profile Completion
      ↓
 ┌───────────────┬────────────────────┐
 ↓                                    ↓
Search                          Recommendation
 ↓                                    ↓
Name / Skill              Feedback Rate · Category ·
                           Desired ↔ Acquired Skills ·
                           Skill Level Mapping
 └───────────────┬────────────────────┘
                  ↓
          Request Sent to User
                  ↓
           "Accept or not?"
             /          \
           NO            YES
            ↓              ↓
  Request Rejected        Chat
                            ↓
                       Scheduling
                            ↓
                        Feedback
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Frontend** | ![React](https://img.shields.io/badge/-React-149eca?style=flat-square&logo=react&logoColor=white) ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) |
| **Backend** | ![Flask](https://img.shields.io/badge/-Flask-000000?style=flat-square&logo=flask&logoColor=white) ![Python](https://img.shields.io/badge/-Python%203.12.x-3776AB?style=flat-square&logo=python&logoColor=white) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/-Neon%20PostgreSQL-00E599?style=flat-square&logo=postgresql&logoColor=white) |

</div>

---

## 🏗️ System Architecture

```
                    USER
                     │
                     ↓
              React Frontend
                     │
              HTTP / API Requests
                     │
                     ↓
               Flask Backend
                     │
       ┌─────────────┼──────────────┐
       ↓             ↓              ↓
   Search       Recommendation   Application
   Engine          Engine          Logic
       │             │              │
       └─────────────┼──────────────┘
                     │
                     ↓
                Neon PostgreSQL
                     │
       ┌─────────────┼───────────────┐
       ↓             ↓               ↓
    Users/Skills  Connections    Schedule/Feedback
```

> **Note:** This is the logical architecture derived from the confirmed technology stack. A formal architecture diagram has not yet been supplied and should become the authoritative reference once available.

---

## 🗄️ Database Schema

**Database:** Neon PostgreSQL

<div align="center">

![Users](https://img.shields.io/badge/USERS-table-333?style=flat-square)
![Category](https://img.shields.io/badge/CATEGORY-table-333?style=flat-square)
![Skills](https://img.shields.io/badge/SKILLS-table-333?style=flat-square)
![Connection](https://img.shields.io/badge/CONNECTION-table-333?style=flat-square)
![Schedule](https://img.shields.io/badge/SCHEDULE-table-333?style=flat-square)
![Feedback](https://img.shields.io/badge/FEEDBACK-table-333?style=flat-square)

</div>

### USERS
| Field | Type | Notes |
|---|---|---|
| user_id | UUID | Primary Key |
| name | VARCHAR | |
| email | VARCHAR | Unique |
| password_hash | VARCHAR | Hashed only, never plain text |
| avg_rating | NUMERIC | Derived from FEEDBACK |

### CATEGORY
| Field | Type | Notes |
|---|---|---|
| category_id | SERIAL | Primary Key |
| category_name | VARCHAR | Unique |

### SKILLS
| Field | Type | Notes |
|---|---|---|
| skill_id | UUID | Primary Key |
| user_id | UUID | FK → USERS |
| category_id | INT | FK → CATEGORY |
| skill | VARCHAR | Offered skill |
| skill_level | VARCHAR | Offered proficiency |
| desired_skill | VARCHAR | Target skill |
| desired_level | VARCHAR | Target proficiency |

### CONNECTION
| Field | Type | Notes |
|---|---|---|
| connection_id | UUID | Primary Key |
| user_id | UUID | FK |
| connection_user_id | UUID | FK |
| chat_locked | BOOLEAN | Default `TRUE` |
| chat_data | JSONB | Messages array |
| status | VARCHAR | `PENDING` / `ACTIVE` / `COMPLETED` |

### SCHEDULE
| Field | Type | Notes |
|---|---|---|
| schedule_id | UUID | Primary Key |
| user_id | UUID | FK |
| number_of_slot | INT | |
| start | TIMESTAMP | |
| end | TIMESTAMP | |
| agenda | TEXT | |

### FEEDBACK
| Field | Type | Notes |
|---|---|---|
| feedback_id | UUID | Primary Key |
| user_id | UUID | FK → Target user |
| reviewer_user_id | UUID | FK → Reviewer |
| no_of_star | INT | 1–5 |
| feedback_text | TEXT | |

### Entity Relationships

```
                 CATEGORY
                    │  1:N
                    ↓
                  SKILLS
                    ↑  N:1
                   USER
              /      |       \
             ↓       ↓        ↓
      CONNECTION   SCHEDULE   FEEDBACK
```

---

## 🎯 Recommendation Engine

> **Search** = "Find what I ask for."
> **Recommendation** = "Find what is likely to be suitable for me."

### Pipeline

```
Logged-in User → Read Profile → Read Offered/Desired Skills →
Read Skill Levels → Read Categories → Retrieve Candidates →
Remove Ineligible Users → Compare Desired ↔ Offered Skills →
Compare Skill Levels → Compare Categories → Consider Feedback →
Calculate Match Score → Sort → Return Top Recommendations
```

### Match Score Model (proposed)

```
Match Score =
    Skill Compatibility
  + Skill-Level Compatibility
  + Category Compatibility
  + Feedback/Rating Factor
  + Mutual Skill-Swap Compatibility
```

Exact weightings are configurable and should be finalized before production deployment (see [Open Decisions](#-open-decisions)).

### Eligibility Rules
- Never recommend a user to themselves
- Candidate must exist and have relevant skill data
- Respect business rules on rejected/duplicate candidates
- Normalize skills and compare categories by ID

---

## 🔌 API Structure

```
/api/auth            login, register, logout
/api/users            profile, user details
/api/skills           add, update, delete, list
/api/search           by name, by skill
/api/recommendations  get recommendations, calculate match score
/api/connections      send, accept, reject, list
/api/chat             get messages, send message
/api/schedules        create, update, list
/api/feedback         submit, retrieve
```

---

## ✅ MVP Scope

- Authentication (registration, secure login)
- Profile completion (offered/desired skills + levels)
- Search (by name, by skill)
- Recommendation engine (global matching, skill/level/category compatibility, rating factor, match score)
- Requests (send, accept, reject, connection status)
- Chat after accepted connection
- Scheduling (start/end time, slots, agenda)
- Feedback (1–5 stars, written review, average rating)

---

## 🚀 Future Roadmap

Post-MVP considerations, not required for initial release:

- Real-time chat via WebSockets
- Real-time and email/push notifications
- Calendar integration & video meetings
- ML-based advanced matching
- Skill verification and certificates
- Learning progress tracking / session history
- Admin dashboard, report/block functionality
- Advanced filters, location-based campus matching
- Skill popularity analytics
- Recommendation explanations
- User reputation system

---

## 🚫 Out of Scope

Unless explicitly added to scope, the following are **not** part of the MVP:

- Paid courses / payment processing
- External instructors or a commercial marketplace
- Professional certification
- Automated teaching content generation
- External social-media integration
- AI chatbot or video conferencing

CrossSkill's core purpose is **peer-to-peer student skill exchange**, not a course marketplace.

---

## 📋 Development Order

```
1. Project Setup           →  8. Category + Skill Mgmt   →  15. Feedback
2. Neon Database             9. Search Engine               16. Average Rating
3. Database Tables          10. Recommendation Engine       17. Testing
4. Flask Backend Setup      11. Connection Requests         18. Integration
5. React Frontend Setup     12. Accept/Reject               19. Deployment
6. Authentication           13. Chat
7. Profile Management       14. Scheduling
```

**Dependency chain:** `Authentication → Profile → Skills → Recommendation`
**Lifecycle chain:** `Connection → Chat → Scheduling → Feedback`

---

## 🔒 Security & Privacy

- Passwords stored only as hashes — never plain text
- Neon connection credentials kept in environment variables, never hard-coded
- API input validated on every request
- Authenticated routes protected; users cannot modify another user's profile
- Search and recommendation responses never expose `password_hash` or credentials
- Connection ownership validated before chat access is granted
- Ratings constrained to `1 ≤ rating ≤ 5`

---

## ❓ Open Decisions

The following items are **intentionally undefined** in the current PRD and should be finalized during implementation rather than assumed:

1. Exact match-score formula and weight percentages
2. Exact skill-level scale (e.g., Beginner/Intermediate/Advanced vs. numeric)
3. Authentication mechanism
4. Final API endpoint naming
5. React folder/component structure
6. Flask project structure
7. Neon connection/ORM library
8. Real-time chat implementation
9. Notification mechanism
10. Scheduling conflict rules
11. Rules for re-sending rejected requests
12. Feedback eligibility rules
13. Final architecture diagram and any external services
14. UI design system (colors, typography)
15. Deployment platform

---

## 📊 Project Status

<div align="center">

| Item | Status |
|---|---|
| User Flow Diagram | ✅ Provided |
| ER Diagram | ✅ Provided |
| PRD | ✅ v1.0 Complete |

</div>

**Success is defined as:** a student can create an account, complete their profile, add offered/desired skills, discover a partner via search or recommendation, send and have a request accepted, chat, schedule a session, complete it, and leave feedback that contributes to the partner's reputation.

---

<div align="center">

<sub>This README is derived from the CrossSkill PRD (v1.0, 19 August 2026) and should be kept in sync with the PRD, User Flow, ER Diagram, and Architecture Diagram as the project evolves.</sub>

</div>
