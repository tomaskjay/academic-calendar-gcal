## Case Academic Calendar GCal Generator

Made this because Case doesn't allow making a GCal from the academic calendar dates on its [site](https://case.edu/registrar/dates-deadlines/academic-calendar) like they do with course schedules on SIS. Saves time by scraping the page based on an input of any academic session and creates an importable url.

## Setup

### Prereqs
1. **Python 3.6+**: Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
2. **Google Cloud Project**: Set up a Google Cloud project and enable the Google Calendar API. Follow the instructions [here](https://developers.google.com/calendar/quickstart/python) to create a service account and download the `client_secret.json` file.

### Steps
1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a [.env](http://_vscodecontentref_/1) file in the project root directory.
    - Add the following line to the [.env](http://_vscodecontentref_/2) file:
      ```env
      GOOGLE_APPLICATION_CREDENTIALS=client_secret.json
      ```

5. **Run the script**:
    ```sh
    python generate_gcal.py
    ```

### Usage
1. When prompted, enter the session and year (e.g., 'Fall 2024')
2. The script scrapes the academic calendar, creates a new GCal, and adds the events to it. 
3. You just have to import the link it gives in the terminal into Google Calendar

### Notes
- It's important that the [client_secret.json](http://_vscodecontentref_/3) file is in the project root directory.
- The script uses the Google Calendar API to create and manage calendars. Make sure your Google Cloud project has the necessary permissions.

### Examples (URL's to import):

Spring 2025:
https://calendar.google.com/calendar/ical/bd5ec77f65385d1da0307e23b4f5c71cf06c9e7e8f701275c65a2e0ca5f4bcb8@group.calendar.google.com/public/basic.ics

Fall 2025:
https://calendar.google.com/calendar/ical/70ac8fc4c27fbd29dd135576f951a8c810c14e839590491497c81293157635d9@group.calendar.google.com/public/basic.ics

Spring 2026:
https://calendar.google.com/calendar/ical/7c600d2d9b5c6377e8f0ebab281397e5644fb6e1c2214bf16f8f9c1e06b52d0b@group.calendar.google.com/public/basic.ics