def get_enac_ics(downloadPath, icsPath, url, user, password, nombre_de_mois):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from time import sleep
    import shutil
    import os

    #nous devrions vérifier si le fichier existe ou non avant de le supprimer.
    print("processing", nombre_de_mois, "month" if nombre_de_mois > 1 else "months")
    if os.path.exists(icsPath + "/planning.ics"):
        print("Suppression du fichier: ", icsPath + "/planning.ics")
        os.remove(icsPath + "/planning.ics")
    else:
        print("Impossible de supprimer le fichier planning.ics car il n'existe pas")
    for i in range(1,nombre_de_mois):
        if os.path.exists(icsPath + f"/planning ({i}).ics"):
            os.remove(icsPath + f"/planning ({i}).ics")
        else:
            print(f"Impossible de supprimer le fichier planning ({i}).ics car il n'existe pas")
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')  # Run browser in headless mode
    #browser_locale = 'fr'
    #chrome_options.add_argument("--lang={}".format(browser_locale))
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    if driver.find_element(By.ID, "j_idt30:j_idt40_label").text != "Français":
        driver.find_element(By.XPATH, "//div[@class='ui-selectonemenu-trigger ui-state-default ui-corner-right']").click()
        sleep(2)
        driver.find_element(By.ID, "j_idt30:j_idt40_1").click()
        sleep(2)
        alert = Alert(driver)
        alert.accept()
        sleep(2)
    driver.find_element(By.ID, "username").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(password)
    sleep(2)
    driver.find_element(By.ID, "j_idt28").click()
    driver.implicitly_wait(10)
    sleep(2)
    try:
        driver.find_element(By.LINK_TEXT, "Mon emploi du temps").click()
    except:
        driver.find_element(By.LINK_TEXT, "My schedule").click()
    driver.implicitly_wait(100)
    sleep(2)
    driver.find_element(By.XPATH, "//button[@class='fc-month-button ui-button ui-state-default ui-corner-left ui-corner-right']").click()
    sleep(5)
    driver.find_element(By.ID, "form:j_idt121").click()
    sleep(2)
    for _ in range(1,nombre_de_mois):
        try:
            print("Téléchargement du planning pour le mois: ", _)
            driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL + Keys.HOME)
            sleep(5)
            driver.find_element(By.XPATH, "//button[@class='fc-next-button ui-button ui-state-default ui-corner-left ui-corner-right']").click()
            sleep(5)
            driver.find_element(By.ID, "form:j_idt121").click()
            sleep(5)
        except:
            print("Erreur lors du téléchargement du planning pour le mois: ", _)
    sleep(2)

    #cut paste the ics file
    if os.path.exists(downloadPath + "/planning.ics"):
        shutil.move(downloadPath + "/planning.ics", icsPath)
    else:
        print("Impossible de déplacer le fichier planning.ics car il n'existe pas")
    for i in range(1,nombre_de_mois):
        if os.path.exists(downloadPath + f"/planning ({i}).ics"):
            shutil.move(downloadPath + f"/planning ({i}).ics", icsPath)
        else:
            print(f"Impossible de déplacer le fichier planning ({i}).ics car il n'existe pas")