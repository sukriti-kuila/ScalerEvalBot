![banner](https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/1b1c387f-355b-47a1-8ecf-671cd6b96854)

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/sukriti-kuila/ScalerEvalBot?color=blue)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/sukriti-kuila/ScalerEvalBot)
![GitHub repo file count (total files)](https://img.shields.io/github/directory-file-count/sukriti-kuila/ScalerEvalBot?label=total%20files)

## How To Run The Project Locally
### Download and Install Python
   - If you haven't already, download and install Python on your local machine. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/).

### Clone the Project Repository
   - Clone the project repository to your local machine using Git. Replace `<repository_url>` with the actual URL of your project's Git repository:
     ```
     git clone <repository_url>
     ```
- Change your current working directory to the  project folder. Replace ```<project_folder>``` with the actual name of the project folder that was created when you cloned the repository

    ```
    cd <project_folder>
    ```
    

**Set Up a Virtual Environment (Optional but Recommended)**
   - Setting up a virtual environment is optional but highly recommended. It isolates your project's dependencies and avoids conflicts with system-wide packages.
- Open a terminal or command prompt.
- Navigate to your project directory using the `cd` command.
- Create a virtual environment:
    ```
      python -m venv venv
    ```
- Activate the virtual environment:
     - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

**Install Project Dependencies**
   - With your virtual environment active (if you're using one), install the project dependencies specified in `requirements.txt` using `pip`:

     ```bash
     pip install -r requirements.txt
     ```
**Create the .env file**
   - Before you can run the project locally, you need to set up a .env file to store sensitive information like API keys and other configuration variables. Follow these steps to create and populate the .env file:

   - Create a file named .env in the root directory of your project. Open the .env file in a text editor and add the following lines, replacing the placeholders with your actual API keys and configuration information:
     ```
     DISCORD_BOT_TOKEN=your_discord_bot_token
     DB_URI_STRING=your_database_uri
     TATSU_API_TOKEN=your_tatsu_api_token
      ```


**Run The Project**
   - You can now run the project locally as you normally would. Use the appropriate command to execute your project. For example, if your project's entry point is a Python script, you can run it using:
     ```bash
     python your_script.py
     ```
   - Replace `your_script.py` with the actual name of your project's main script.

_Note: In order to run ```/help``` command change the ```testserverid``` in ```main.py``` variable to the desired server id_
## Commands

- ### Add A New Event
    **Only admins** can access this command. Follow these steps to set up a new event:
    ``` 
    !evalbot new event
    <event name>
    <event start date[DD-MM-YYYY] [SPACE] start time[HH:MM:SS]>
    <event duration>
    ```
    #### Example
  ![AddEvent_command](https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/9b4982cb-6b50-44b0-8ebc-0c7ffb9d0e27)

    
    After running the command, make sure to create a channel on Discord with the same name as the event name. The channel name is case-insensitive. Participants will send their daily posts to the respective channels, which will be automatically set up for each event.

    Only admins can create a new event, and participants will use the designated channels for daily post submissions.

     ### Reminder
   In case, someone forgets to post a daily task on Discord, the bot will send one reminder automatically **approx 1 hour** before.
  #### Example
   <img width="437" alt="Screenshot 2023-10-15 235618" src="https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/e0b9c114-c81c-43ba-9978-454ef98414b2">

  #### Note
     Do not upload the CSV file with scientific notation (eg: 6.73929E+17)
  
     <img width="416" alt="Screenshot 2023-10-16 212657" src="https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/0859907e-1a79-4224-a78a-d3709d1120ef">
      
   
- ### Format For Daily Post 
    To submit your daily task, please follow the format below. The bot will validate your submission, and if it's correct, you'll receive a confirmation message. In case of any mistakes, the bot will guide you for corrections. Replace the placeholders ```<day number>```, ```<X (Twitter) or Linkedin Post Link>```, and ```<Screenshot of the task>``` with the actual information.
    #### Format
    ```
    !evalbot Completed Day<day number>
    Social Media Link : <X (Twitter) or Linkedin Post Link>
    <Screenshot of the task>
    ```
    #### Example
    <img width="579" alt="format_check" src="https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/2c87ab69-d084-4643-91d2-1ada798fca89">

   #### Disqualify
  
   In case you skip one day and try to post it on the next day following message will be shown
   <img width="580" alt="misses_a_day" src="https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/eb47ce71-aa09-4d87-867d-3fc121e264f6">


- ### Delete An Event
    Only admins can delete an event.
    #### Format
    ```
    !evalbot delete event
    <event name>
    ```
    #### Example
  <img width="535" alt="Delete_command" src="https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/7a549c3c-7331-42cf-aeba-c973f910fd8f">


- ### Result of An Event
    To obtain the lists of both **eligible** and **non-eligible** participants who have posted daily tasks throughout the event, you can use this command. Please note that **only admins** can use this command. The generated CSV files will be sent to the admin's DM.
    #### Format
    ```
    !evalbot res event
    <event name>
    ```
    #### Example
     <img width="550" alt="result" src="https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/7b7d387f-03b5-42d7-8292-3004cedfc16f">
     <img width="500" alt="result_dm" src="https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/fa47d7ae-3c5e-4ac4-993a-bece8555bbb3">




- ### Update Token
    This command allows to add tokens from participant accounts. Please note that **only admins** can use this command. 
    
    Please make sure to replace ```<token amount>``` with the desired amount of tokens to add or deduct, and ```<csv file>``` with the name of the CSV file containing the list of participants. Here's how to use it:
    #### Format
    ```
    !evalbot update token
    <token amount>
    <CSV File>
    ```
    #### Example
    <img width="535" alt="updateToken_command" src="https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/0abb0e65-1334-4b15-90e4-42b4e1b93bc5">


- ### /help
    To get assistance and view the formats of all available commands, you can use the **/help** command. This command will provide you with a comprehensive list of available commands and their formats.
  #### Example
  <img width="618" alt="help_command" src="https://github.com/sukriti-kuila/ScalerEvalBot/assets/87015685/749cb4b7-5058-4ea1-b722-fae80ce87e48">

     
