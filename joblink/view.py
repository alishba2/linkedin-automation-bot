# your_app_name/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import utils
from . import constants
from . import config

import time
import random
import os
import pickle
import hashlib
import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


@csrf_exempt
def apply_to_jobs(request):
    if request.method == 'POST':
        try:
            # Run the LinkedIn automation code directly in the view
            utils.prYellow("🤖 Thanks for using Easy Apply Jobs bot, for more information you can visit our site - www.automated-bots.com")
            utils.prYellow("🌐 Bot will run in Chrome browser and log in Linkedin for you.")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=utils.chromeBrowserOptions())
            cookies_path = f"{os.path.join(os.getcwd(),'cookies')}/{getHash(config.email)}.pkl"
            driver.get('https://www.linkedin.com')
            # loadCookies(driver, cookies_path)

            if not isLoggedIn(driver):
                driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
                utils.prYellow("🔄 Trying to log in Linkedin...")
                try:
                    driver.find_element("id", "username").send_keys(config.email)
                    time.sleep(2)
                    driver.find_element("id", "password").send_keys(config.password)
                    time.sleep(2)
                    driver.find_element("xpath", '//button[@type="submit"]').click()
                    time.sleep(30)
                except:
                    utils.prRed("❌ Couldn't log in Linkedin by using Chrome. Please check your Linkedin credentials on config files line 7 and 8.")

                # saveCookies(driver, cookies_path)
            # start application
            linkJobApply(driver)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def getHash(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def loadCookies(driver, cookies_path):
    if os.path.exists(cookies_path):
        cookies = pickle.load(open(cookies_path, "rb"))
        driver.delete_all_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)


def saveCookies(driver, cookies_path):
    pickle.dump(driver.get_cookies(), open(cookies_path, "wb"))


def isLoggedIn(driver):
    driver.get('https://www.linkedin.com/feed')
    try:
        driver.find_element(By.XPATH, '//*[@id="ember14"]')
        return True
    except:
        pass
    return False


def generateUrls():
    if not os.path.exists('data'):
        os.makedirs('data')
    try:
        with open('data/urlData.txt', 'w', encoding="utf-8") as file:
            linkedinJobLinks = utils.LinkedinUrlGenerate().generateUrlLinks()
            for url in linkedinJobLinks:
                file.write(url + "\n")
        utils.prGreen("✅ Apply urls are created successfully, now the bot will visit those urls.")
    except:
        utils.prRed("❌ Couldn't generate urls, make sure you have edited config file line 25-39")


def linkJobApply(driver):
    generateUrls()
    countApplied = 0
    countJobs = 0

    urlData = utils.getUrlDataFile()

    for url in urlData:
        driver.get(url)
        time.sleep(random.uniform(1, constants.botSpeed))

        totalJobs = driver.find_element(By.XPATH, '//small').text
        totalPages = utils.jobsToPages(totalJobs)

        urlWords = utils.urlToKeywords(url)
        lineToWrite = "\n Category: " + urlWords[0] + ", Location: " + urlWords[1] + ", Applying " + str(
            totalJobs) + " jobs."
        displayWriteResults(lineToWrite)

        for page in range(totalPages):
            currentPageJobs = constants.jobsPerPage * page
            url = url + "&start=" + str(currentPageJobs)
            driver.get(url)
            time.sleep(random.uniform(1, constants.botSpeed))

            offersPerPage = driver.find_elements(
                By.XPATH, '//li[@data-occludable-job-id]')
            offerIds = [(offer.get_attribute(
                "data-occludable-job-id").split(":")[-1]) for offer in offersPerPage]
            time.sleep(random.uniform(1, constants.botSpeed))

            for offer in offersPerPage:
                if not element_exists(offer, By.XPATH, ".//*[contains(text(), 'Applied')]"):
                    offerId = offer.get_attribute("data-occludable-job-id")
                    offerIds.append(int(offerId.split(":")[-1]))

            for jobID in offerIds:
                offerPage = 'https://www.linkedin.com/jobs/view/' + str(jobID)
                driver.get(offerPage)
                time.sleep(random.uniform(1, constants.botSpeed))

                countJobs += 1

                jobProperties = getJobProperties(driver, countJobs)
                if "blacklisted" in jobProperties:
                    lineToWrite = jobProperties + " | " + "* 🤬 Blacklisted Job, skipped!: " + str(offerPage)
                    displayWriteResults(lineToWrite)

                else:
                    easyApplybutton = easyApplyButton(driver)

                    if easyApplybutton is not False:
                        easyApplybutton.click()
                        time.sleep(random.uniform(1, constants.botSpeed))

                        try:
                            chooseResume(driver)
                            driver.find_element(By.CSS_SELECTOR,
                                               "button[aria-label='Submit application']").click()
                            time.sleep(random.uniform(1, constants.botSpeed))

                            lineToWrite = jobProperties + " | " + "* 🥳 Just Applied to this job: " + str(offerPage)
                            displayWriteResults(lineToWrite)
                            countApplied += 1

                        except:
                            try:
                                driver.find_element(
                                    By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
                                time.sleep(random.uniform(1, constants.botSpeed))
                                chooseResume(driver)
                                comPercentage = driver.find_element(
                                    By.XPATH, 'html/body/div[3]/div/div/div[2]/div/div/span').text
                                percenNumber = int(comPercentage[0:comPercentage.index("%")])
                                result = applyProcess(driver, percenNumber, offerPage)
                                lineToWrite = jobProperties + " | " + result
                                displayWriteResults(lineToWrite)

                            except Exception:
                                chooseResume(driver)
                                lineToWrite = jobProperties + " | " + \
                                    "* 🥵 Cannot apply to this Job! " + str(offerPage)
                                displayWriteResults(lineToWrite)
                    else:
                        lineToWrite = jobProperties + " | " + "* 🥳 Already applied! Job: " + str(offerPage)
                        displayWriteResults(lineToWrite)

        utils.prYellow("Category: " + urlWords[0] + "," + urlWords[1] + " applied: " + str(countApplied) +
                      " jobs out of " + str(countJobs) + ".")

    utils.donate(driver)


def chooseResume(driver):
    try:
        driver.find_element(
            By.CLASS_NAME, "jobs-document-upload__title--is-required")
        resumes = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'ui-attachment--pdf')]")
        if (len(resumes) == 1 and resumes[0].get_attribute("aria-label") == "Select this resume"):
            resumes[0].click()
        elif (len(resumes) > 1 and resumes[config.preferredCv-1].get_attribute("aria-label") == "Select this resume"):
            resumes[config.preferredCv-1].click()
        elif (type(len(resumes)) != int):
            utils.prRed(
                "❌ No resume has been selected please add at least one resume to your Linkedin account.")
    except:
        pass


def getJobProperties(driver, count):
    textToWrite = ""
    jobTitle = ""
    jobLocation = ""

    try:
        jobTitle = driver.find_element(
            By.XPATH, "//h1[contains(@class, 'job-title')]").get_attribute("innerHTML").strip()
        res = [blItem for blItem in config.blackListTitles if (
            blItem.lower() in jobTitle.lower())]
        if (len(res) > 0):
            jobTitle += "(blacklisted title: " + ' '.join(res) + ")"
    except Exception as e:
        if (config.displayWarnings):
            utils.prYellow("⚠️ Warning in getting jobTitle: " + str(e)[0:50])
        jobTitle = ""

    try:
        time.sleep(5)
        jobDetail = driver.find_element(By.XPATH, "//div[contains(@class, 'job-details-jobs')]//div").text.replace(
            "·", "|")
        res = [blItem for blItem in config.blacklistCompanies if (
            blItem.lower() in jobTitle.lower())]
        if (len(res) > 0):
            jobDetail += "(blacklisted company: " + ' '.join(res) + ")"
    except Exception as e:
        if (config.displayWarnings):
            print(e)
            utils.prYellow(
                "⚠️ Warning in getting jobDetail: " + str(e)[0:100])
        jobDetail = ""

    try:
        jobWorkStatusSpans = driver.find_elements(By.XPATH, "//span[contains(@class,'ui-label ui-label--accent-3 text-body-small')]//span[contains(@aria-hidden,'true')]")
        for span in jobWorkStatusSpans:
            jobLocation = jobLocation + " | " + span.text

    except Exception as e:
        if (config.displayWarnings):
            print(e)
            utils.prYellow(
                "⚠️ Warning in getting jobLocation: " + str(e)[0:100])
        jobLocation = ""

    textToWrite = str(count) + " | " + jobTitle + " | " + jobDetail + jobLocation
    return textToWrite


def easyApplyButton(driver):
    try:
        time.sleep(random.uniform(1, constants.botSpeed))
        button = driver.find_element(By.XPATH, "//div[contains(@class,'jobs-apply-button--top-card')]//button[contains(@class, 'jobs-apply-button')]")
        EasyApplyButton = button
    except:
        EasyApplyButton = False

    return EasyApplyButton


def applyProcess(driver, percentage, offerPage):
    applyPages = math.floor(100 / percentage) - 2
    result = ""
    for pages in range(applyPages):
        driver.find_element(
            By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()

    driver.find_element(By.CSS_SELECTOR,
                       "button[aria-label='Review your application']").click()
    time.sleep(random.uniform(1, constants.botSpeed))

    if config.followCompanies is False:
        try:
            driver.find_element(
                By.CSS_SELECTOR, "label[for='follow-company-checkbox']").click()
        except:
            pass

    driver.find_element(
        By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
    time.sleep(random.uniform(1, constants.botSpeed))

    result = "* 🥳 Just Applied to this job: " + str(offerPage)

    return result


def displayWriteResults(lineToWrite: str):
    try:
        print(lineToWrite)
        utils.writeResults(lineToWrite)
    except Exception as e:
        utils.prRed("❌ Error in DisplayWriteResults: " + str(e))


def element_exists(parent, by, selector):
    return len(parent.find_elements(by, selector)) > 0


start = time.time()
end = time.time()
utils.prYellow("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
