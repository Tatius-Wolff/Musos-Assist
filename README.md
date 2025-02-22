# Musos-Assist

**A platform for musicians and artists to release and promote their art on a regular cadence.**

## Project Description

Musos-Assist is designed to empower musicians and artists by providing a centralised platform for managing their releases, from content creation to promotion and fan engagement. This platform aims to streamline the release process, enabling artists to maintain a consistent output and build stronger connections with their audience.

**Key Features (MVP):**

* **Release Management:** Track releases end-to-end, grouping all related artifacts.
* **Content Upload:** Upload and manage music, artwork, videos, and lyrics.
* **User Authentication:** Secure user registration and login.
* **Artifact Grouping:** Group cover artwork, audio mixes, and videos with their respective releases.
* **Lyrics Storage:** Store lyrics alongside releases for easy access.

**Future Features (Post-MVP):**

* Hierarchical Release Bundling
* Release Profile Templates
* Merchandise Tracking
* Artwork Format Conversion
* Collaboration Features
* Release Scheduling
* Metadata Management (Tags, Keywords)
* Drafting and Previewing
* Version Control
* Credits and Contributor Management
* Import/Export Functionality
* Embeddable Content
* Shareable Links
* Promotional Material Generation
* Release Performance Analytics
* Email Marketing Integration
* Social Media Integration
* Pre-save Campaigns
* Fan Following and Notifications
* Commenting and Sharing
* Merchandise Purchasing
* Playlists and Exclusive Content
* User Management (Admin)
* Platform Monitoring (Admin)
* Subscription Management (Admin)
* Content Moderation (Admin)
* Reporting (Admin)
* WCAG Compliance
* Mobile Responsiveness
* Multi Factor Authentication

## Getting Started

### Prerequisites

* Python 3.x
* PostgreSQL
* Other dependencies TBA

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/Tatius-Wolff/Musos-Assist.git
    cd Musos-Assist
    ```

2.  Create a virtual environment and install dependencies:

    ```bash
    python3 -m poetry install
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  Configure your database:

    * Create a PostgreSQL database.
    * Update the database connection settings in your application's configuration file.

4.  Run database migrations:

    ```bash
    # (If using Django or similar ORM)
    python manage.py migrate
    ```

6.  Start the application:

    ```bash
    # (Example for FastAPI)
    uvicorn main:app --reload
    ```

## Usage

1.  Navigate to the application in your web browser.
2.  Register a new account or log in.
3.  Create a new release and upload your content.
4.  Manage your releases and artifacts.

## Technology Stack

* **Backend:** Python (FastAPI)
* **Database:** PostgreSQL
* **Frontend:** HTML/CSS (Bootstrap/Tailwind CSS)
* **Cloud Storage:** [e.g., AWS S3, Google Cloud Storage]
* **Development Tools:** Git, VS Code

## Non-Functional Requirements

* **Performance:**
    * Uploads within 2 minutes (up to 10GB).
    * Retrieval within 30 seconds.
    * Scalable to 10 concurrent users (Post-MVP).
* **Security:**
    * User authentication (MVP: strong passwords, Post-MVP: MFA).
    * Data encryption.
    * Hourly backups.
    * Access control.
* **Usability:**
    * Intuitive interface.
    * Easy navigation.
    * Mobile responsiveness (Post-MVP).
    * WCAG compliance (Post-MVP).
* **Reliability:**
    * 99% uptime (MVP), 99.9% uptime (Post-MVP).
    * Redundancy and failover mechanisms.
    * Data consistency.
* **Maintainability:**
    * Clean code, clear documentation.
    * Automated testing and CI/CD.
    * Vulnerability scanning.
* **Compatibility:**
    * Windows, macOS, Linux.
    * Chrome/Chromium browsers.
    * PNG, FLAC, MP4, HEVC file formats.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them.
4.  Push your changes to your fork.
5.  Submit a pull request.

## License

GNU GENERAL PUBLIC LICENSE Version 3

## Contact

Stephan Borg (tatius.wolff at gmail.com)