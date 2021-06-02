from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler

TOKEN = insert yours here 
CHAT = insert yours here
websites = {"AUSL Parma": {"url": "https://www.ausl.pr.it/comunicazione_stampa/ultimo_mese/default.aspx", "element": "#paginaindice"},
            "AUSL Modena": {"url": "http://www.ausl.mo.it/archivio-in-primo-piano", "element": ".ElencoSemplice"},
            "AUSL Bologna": {"url": "https://www.ausl.bologna.it", "element": "#content"},
            "AUSL Ferrara":  {"url": "https://www.ausl.fe.it/home-web", "element": ".portlet"},
            "AUSL Reggio":  {"url": "https://www.ausl.re.it/comunicazione/comunicati-stampa", "element": ".view-content"}
            }


def start(update, context):
    '''reply to /start cmd'''
    print(update.message.chat_id)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Correctly printed your chat ID\n")


options = Options()

options.headless = False
driver = webdriver.Firefox(options=options)
prev_html = {}
# fill the prev htmls
for name, website in websites.items():
    driver.get(website["url"])
    prev_html[website["url"]] = driver.find_element_by_tag_name(
        website["element"]).get_attribute("innerHTML").lower()
    print(prev_html)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
# Then, loop and check for open days
while True:
    for name, website in websites.items():
        driver.get(website["url"])
        actual_html = driver.find_element_by_tag_name(
            website["element"]).get_attribute("innerHTML").lower()
        if actual_html != prev_html[website["url"]]:
            print(
                f"Found difference on {name}. Checking if the page talks about open days.")
            if "open day" in actual_html or "openday" in actual_html:
                print("Found open day in the page! Sending a text")
                text = f"Check [{name}]("+website["url"]+") for a new open day"
                updater.bot.send_message(
                    chat_id=CHAT, text=text, parse_mode=ParseMode.MARKDOWN)
        prev_html[website["url"]] = actual_html
