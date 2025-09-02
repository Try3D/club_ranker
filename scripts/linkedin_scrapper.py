from linkedin_scraper import Company, actions
from selenium import webdriver

driver = webdriver.Chrome()

email = "xxxxxxxxxxx@gmail.com"
password = "xxxxxxxxxxxx"
actions.login(driver, email, password)

companies = [
    "https://www.linkedin.com/company/snuc-dance-club/?originalSubdomain=in",
    "https://www.linkedin.com/company/cognition-the-snuc-quiz-club/",
    "https://www.linkedin.com/company/snuc-potential/",
    "https://www.linkedin.com/company/snuc-coding-club/",
    "https://www.linkedin.com/company/the-business-club-snu-chennai/",
    "https://www.linkedin.com/company/isai-snuc-music-club/",
    "https://www.linkedin.com/company/aura-snuc-design-club/",
]

for company in companies:
    scrapper = Company(
        company,
        driver=driver,
    )

    scrapper.scrape()
