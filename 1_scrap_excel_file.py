from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Explicit Waits 사용을 위한 라이브러리
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time


# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
driver.implicitly_wait(5)  # 웹페이지가 로딩 될때까지 5초 기다림
driver.maximize_window()  # 화면 최대화

post_no = str()
page_now = str()
sch_nm = str()


def incheon_school_scraping():

    # 시작. 인천광역시 교육청 홈페이지로 출발
    driver.get("http://www.ice.go.kr/main.do?s=ice")
    time.sleep(1)

    # 부서홈페이지
    driver.find_element(By.XPATH, '//dt/a/span[text()="부서홈페이지"]').click()
    time.sleep(1)

    # 학교생활교육과
    driver.find_element(By.XPATH, '//li/a[@title="학교생활교육과"]').click()
    time.sleep(1)

    # 무상교육공개방
    driver.find_element(By.XPATH, '//a/span[text()="무상 교복 공개방"]').click()
    time.sleep(1)

    # 마지막 페이지로 가서 게시물을 뒤에서 훑어온다.
    driver.find_element(By.XPATH, '//div/p/span/a/img[@title="끝페이지"]').click()
    time.sleep(1)

    """ 중단되었을 경우 재개용 코드 """
    # driver.find_element(
    #     By.XPATH,
    #     '//*[@id="subContent"]/div/div/form[1]/div/div/p/span/a[contains(@href,"page=5")]',
    # ).click()
    # time.sleep(1)

    """ """

    # 페이지 확인 (for문 범위 잡기 위해 한 번 확인)
    page_now = driver.find_element(
        By.XPATH, "//*[@id='subContent']/div/div/form[1]/div/div[4]/p/span[1]/strong"
    ).text

    for i in range(int(page_now), 0, -1):  # 페이지 돌리기

        for j in range(1, 11):  # 게시물 돌리기

            # 게시물 번호 출력
            try:
                post_no = driver.find_element(By.XPATH, f"//tbody/tr[{j}]/td[1]").text
                sch_nm = driver.find_element(By.XPATH, f"//tbody/tr[{j}]/td[3]").text

                print(f"{post_no} 번 게시물 진행중     ->    {sch_nm}")
            except NoSuchElementException:
                break

            # 게시물 클릭 1~10
            # driver.find_element(
            #     By.XPATH, f'//tbody/tr[{j}]/td/a[@href="#contents"]'
            # ).click()
            # time.sleep(1)

            # 명시적 대기 적용
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//tbody/tr[{j}]/td/a[@href="#contents"]')
                )
            ).click()
            time.sleep(1)

            # 첨부파일 갯수 표시 (2개 이상일 경우만)
            files = driver.find_elements(
                By.XPATH,
                '//dl/dd/a[contains(text(),"xlsx") or contains(text(),"hwp")]',
            )

            if len(files) >= 1:
                if len(files) > 1:
                    print(f"첨부파일이 {len(files)} 개 이상 입니다.")

                # 첨부파일 클릭 반복문 (step이 2인 이유는 중간중간에 바로보기 태그가 끼어들어가 있음)
                for f in range(1, len(files) * 2, 2):
                    # driver.find_element(
                    #     By.XPATH,
                    #     f'//dl/dd/a[{f}][contains(text(),"xlsx") or contains(text(),"hwp")]',
                    # ).click()
                    # time.sleep(1)

                    # 명시적 대기
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                f'//dl/dd/a[{f}][contains(text(),"xlsx") or contains(text(),"hwp")]',
                            )
                        )
                    ).click()
            else:
                print("첨부파일이 없습니다.")

            # 목록 버튼 눌러 복귀
            # driver.find_element(By.XPATH, "//article/div/a[@class='gray']").click()
            # time.sleep(1)

            # 명시적 대기
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//article/div/a[@class='gray']")
                )
            ).click()
            time.sleep(1)

        # 현재 페이지 표시
        page_now = driver.find_element(
            By.XPATH,
            "//*[@id='subContent']/div/div/form[1]/div/div[4]/p/span[1]/strong",
        ).text

        print(f"{page_now} 페이지 작업완료")

        # 이전 페이지로
        if page_now == "1":
            print("첫 페이지입니다. 작업이 끝났습니다.")
        else:
            # href 안에 있는 page 파라메터를 추적해서 계속 이전 페이지를 탐색한다.
            # driver.find_element(
            #     By.XPATH,
            #     f'//*[@id="subContent"]/div/div/form[1]/div/div/p/span/a[contains(@href,"page={str(int(page_now)-1)}")]',
            # ).click()
            # time.sleep(1)
            # 명시적 대기
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f'//*[@id="subContent"]/div/div/form[1]/div/div/p/span/a[contains(@href,"page={str(int(page_now)-1)}")]',
                    )
                )
            ).click()


if __name__ == "__main__":
    incheon_school_scraping()
