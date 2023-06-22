## Myges_Scraper

# Description

The project aims to develop a Python bot that scrapes a web page (MyGes) to retrieve the school's course schedule and saves it to Google Calendar. This project is being carried out as part of a course and is a collaborative effort by a team of three.

## Key Features
- Web scraping: The bot utilizes Python's web scraping capabilities to extract the course schedule data from the MyGes web page.
- Data storage: The extracted schedule data is stored using MongoDB, providing a convenient and scalable storage solution.
- Google Calendar integration: The bot integrates with Google Calendar to automatically save the retrieved course schedule, ensuring easy access and synchronization.

## Technologies Used
- Python: The bot is primarily developed using Python programming language, harnessing its extensive libraries and tools.
- MongoDB: The extracted course schedule data is stored in a MongoDB database, providing flexibility and efficiency in data management.
- Docker: The project utilizes Docker to containerize the bot, simplifying deployment and ensuring consistent execution across different environments.

# Installation

To launch the bot using Docker, follow these steps:

1. Make sure you have Docker installed on your system. If not, you can download and install Docker from the official website: https://www.docker.com/get-started.
2. Clone the project repository: `git clone https://github.com/ZK1569/Myges_Scraper.git`
3. Navigate to the project directory: `cd Myges_Scraper`
4. Create a file named `.env` in the project directory.
5. Open the `.env` file and add the following content:
```
TOKEN=<YOUR TOKEN>
MONGO_URL="mongodb://root:passwordRoot@localhost:27017/"
```
6. Save and close the `.env` file.
7. Open a terminal or command prompt and run the following command to build and launch the bot: `docker-compose up --build`
This command will build the Docker image and launch the bot within a Docker container.

    Note: Depending on your system configuration, you may need to run the command with administrative privileges (e.g., sudo docker-compose up --build).

8. The bot should now be up and running, scraping the MyGes web page and saving the course schedule to Google Calendar.

# Usage

The bot provides the following main commands:

- `!me`: Retrieves the user's information.
- `!save <mail> <password>`: Allows the user to save their email and password.
- `!planning`: Requests the bot to update the schedule with the information from MyGes.
- `!ping`: Performs a test ping.
- `!changepassword <password>`: Updates the password.

# License

This project is licensed under the MIT License. See the [LICENSE]() file for details.

# Author

Cristian Ursu - [zk1569](https://github.com/ZK1569)

Loïc ZHU - [LoicZHU](https://github.com/LoicZHU)

Mazene ZERGUINE - [Mazene-ZERGUINE](https://github.com/Mazene-ZERGUINE)