from twisted.internet import task, reactor
from dhooks import Webhook
import fade
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import os
import io
from google.cloud import vision
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

global TOKEN
TOKEN = "OTU5MTc0NjYzNjI2NDUzMDEy.YkYDBA.hhn7-ok5Srj_kpYFluiY-K0hoAs"

def open_webdriver():
    global opts
    global driver
    global wait

    opts = webdriver.ChromeOptions()
    opts.headless = True
    driver = uc.Chrome(use_subprocess=True, options=opts)
    driver.get('https://zefoy.com')
    wait = WebDriverWait(driver, 5)

def captcha_ai():
    open_webdriver()

    global captcha_text
    with open('captcha.png', 'wb') as file:
        captcha = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/form/div/div/img')))
        file.write(captcha.screenshot_as_png)  # write to folder

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"./key.json"
    client = vision.ImageAnnotatorClient()
    with io.open('./captcha.png', 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    text = response.text_annotations[0].description
    captcha_text = text.lower()
    print(fade.pinkred("[* | " + "] Captcha: " + captcha_text), end="\r")
    os.remove('captcha.png')
    WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/form/div/div/div/input'))).send_keys(
        captcha_text, '\n')
    try:
        driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button').click()
        driver.refresh()
    except:
        captcha_ai()


def xfollowers():
    global followers
    global ffloat
    # Followers
    followers = driver.find_element(by=By.XPATH, value="/html/body/div[4]/div[1]/div[3]/div/div[1]/div/p/small")
    if followers.text == "soon will be update":
        ffloat = "Followers are ~~unavailable~~."
        return ffloat
    else:
        ffloat = "**Followers are available.**"
        return ffloat


def xhearts():
    global hearts
    global fhearts
    # Hearts
    hearts = driver.find_element(by=By.XPATH, value="/html/body/div[4]/div[1]/div[3]/div/div[2]/div/p/small")
    if hearts.text == "soon will be update":
        fhearts = "Hearts are ~~unavailable~~."
        return fhearts
    else:
        fhearts = "**Hearts are available.**"
        return fhearts


def xcommenthearts():
    global commenthearts
    global fcommenthearts
    # Comment hearts
    commenthearts = driver.find_element(by=By.XPATH, value="/html/body/div[4]/div[1]/div[3]/div/div[3]/div/p/small")
    if commenthearts.text == "soon will be update":
        fcommenthearts = "Comment hearts are ~~unavailable~~."
        return fcommenthearts
    else:
        fcommenthearts = "**Comment hearts are available.**"
        return fcommenthearts


def xviews():
    global views
    global fviews
    # Views
    views = driver.find_element(by=By.XPATH, value="/html/body/div[4]/div[1]/div[3]/div/div[4]/div/p/small")
    if views.text == "soon will be update":
        fviews = "Views are ~~unavailable~~."
        return fviews
    else:
        fviews = "**Views are available.**"
        return fviews


def xshares():
    global shares
    global fshares
    # Shares
    shares = driver.find_element(by=By.XPATH, value="/html/body/div[4]/div[1]/div[3]/div/div[5]/div/p/small")
    if shares.text == "soon will be update":
        fshares = "Shares are ~~unavailable~~."
        return fshares
    else:
        fshares = "**Shares are available.**"
        return fshares

# load_dotenv()
#
# TOKEN = os.getenv("TOKEN")
timeout = 600

def bot():
    secondsSinceEpoch = time.time()
    timeObj = time.localtime(secondsSinceEpoch)

    hook = Webhook('https://discord.com/api/webhooks/958782740084445184/V2bkfIpTXN-iv7CH6rcERSQniqdu8TTKLw8CQLtewEdF0-rc5-nGCsqBbfNM3LPfg0fG')

    hook.send('**Date:** %d/%d/%d %d:%d:%d' % (
timeObj.tm_mday, timeObj.tm_mon, timeObj.tm_year, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec))
    hook.send(qfollowers)
    hook.send(qhearts)
    hook.send(qcommenthearts)
    hook.send(qviews)
    hook.send(qshares)
    hook.send("-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-")
    pass

if __name__ == "__main__":
    start = True
    print("Starting...")

    # time()
    captcha_ai()
    qfollowers = xfollowers()
    print(qfollowers)
    qhearts = xhearts()
    print(qhearts)
    qcommenthearts = xcommenthearts()
    print(qcommenthearts)
    qviews = xviews()
    print(qviews)
    qshares = xshares()
    print(qshares)
    bot()
    l = task.LoopingCall(bot)
    l.start(timeout)  # call every sixty seconds

    reactor.run()