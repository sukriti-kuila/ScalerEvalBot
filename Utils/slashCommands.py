# Slash commands
async def add_event_command():
    return (
            "```!evalbot new event\n"
            "<event name>\n"
            "<event start date[DD-MM-YYYY] [SPACE] start time[HH:MM:SS]>\n"
            "<event duration>\n"
            "<CSV File>\n```")

async def delete_event_command():
    return (
            "```!evalbot delete event\n"
            "<event name>```\n")        

async def result_event_command():
    return ("```!evalbot res event\n"
            "<event name>```\n"
           )

async def format_check_command():
    return ("```!evalbot Completed Day<day number>\n"
            "Social Media Link : <X (Twitter) or Linkedin Post Link>\n"
            "<Screenshot of the task>```\n"
            )

async def update_token_event_command():
    return ("```!evalbot update token\n"
            "<token amount>\n"
            "<CSV File>```\n"
            "[Click Here To Discover More](https://github.com/sukriti-kuila/ScalerEvalBot)\n"
            )
