## Myges_Scraper

# Description

The project aims to develop a Python bot that scrapes a web page (MyGes) to retrieve the school's course schedule and saves it to Google Calendar. This project is being carried out as part of a course and is a collaborative effort by a team of three.

## Key Features
- Web scraping: The bot utilizes Python's web scraping capabilities to extract the course schedule data from the MyGes web page.
- Data storage: The extracted schedule data is stored using MongoDB, providing a convenient and scalable storage solution.
- Google Calendar integration: The bot integrates with Google Calendar to automatically save the retrieved course schedule, ensuring easy access and synchronization.

## Technologies Used
- Python: The bot is primarily developed using the Python programming language, harnessing its extensive libraries and tools.
- MongoDB: The extracted course schedule data is stored in a MongoDB database, providing flexibility and efficiency in data management.
- Selenium: Selenium is used to automate interactions with the web browser and facilitate scraping of the MyGes web page.
- Docker: The project utilizes Docker to containerize the bot, simplifying deployment and ensuring consistent execution across different platforms.

## Usage

The bot provides the following main commands:

- Auth
  - `!me`: Retrieves the user's information.
  - `!save <mail> <password>`: Allows the user to save their email and password.
  - `/login`:
  - `!bye`: Removes your information from the database 

- Grades 
  - `!notes`: Receive your notes in MP 

- Home Work
  - `!get <date>`: Allows you to have the homework that needs to be done by the date
  - `!add <date> <task>`: Save homework for a specific date

- Schedule
  - `!planning`: Requests the bot to update the schedule with the information from MyGes.

- Trombinoscope
  - `!who <name>`: Allows you to obtain information about a classmate who is in the trombinoscope 
  - `!classe`: Provides a list of all your classmates  
  - `!search`: Get the most up-to-date information from all your classmates 

- Other
  - `!ping`: Performs a test ping.

## Automated Features

In addition to the main commands, the bot includes the following automated features:

- Automatic Trombinoscope Acquisition: The bot automatically fetches and saves the class photos (trombinoscope) from MyGes.
- Daily Calendar Email: The bot sends a daily email containing the day's calendar to the user.


## License

This project is licensed under the MIT License. See the [LICENSE]() file for details.

## Author

Cristian Ursu - [zk1569](https://github.com/ZK1569)

Loïc ZHU - [LoicZHU](https://github.com/LoicZHU)

Mazene ZERGUINE - [Mazene-ZERGUINE](https://github.com/Mazene-ZERGUINE)
