from flask import Flask, render_template, request, redirect, url_for, session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Thiết lập Selenium WebDriver (hiển thị trình duyệt)
chrome_service = Service('./chromedriver-mac-arm64-3/chromedriver')  # Đường dẫn đã được cập nhật

# Khởi tạo driver để giữ session đăng nhập
driver = None

def start_browser():
    global driver
    if driver is None:
        driver = webdriver.Chrome(service=chrome_service)

def login_to_lazada(username, password):
    global driver
    start_browser()  # Khởi động trình duyệt

      # Xử lý username và password
    username = f"097999{username}01"  # Thêm input người dùng vào trước "01"
    password = f"!@Troi{password}roi12"  # Thêm input người dùng vào trước "roi12"

    # Mở trang đăng nhập Lazada
    driver.get("https://pages.lazada.vn/wow/gcp/vn/member/login-signup?redirect=http://adsense.lazada.vn/index.htm")
    time.sleep(3)  # Đợi trang tải xong

    # Nhập username và password
    try:
        username_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Please enter your Phone Number or Email"]')
    except:
        username_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Vui lòng nhập số điện thoại hoặc email của bạn"]')
    username_field.send_keys(username)

    try:
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Please enter your password"]')
    except:
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Vui lòng nhập mật khẩu của bạn"]')
    password_field.send_keys(password)

    # Nhấn nút "Login"
    login_button = driver.find_element(By.CLASS_NAME, 'index_module_loginButton__deb6dcb9')
    login_button.click()
    time.sleep(5)

    # Kiểm tra đăng nhập thành công
    if "adsense.lazada.vn" in driver.current_url:
        return True
    else:
        return False

def convert_link(link_to_convert):
    global driver
    # Sau khi đăng nhập thành công, truy cập trang chuyển đổi link
    driver.get("https://adsense.lazada.vn/index.htm#!/")
    time.sleep(3)

    # Nhấn nút chuyển đổi link
    try:
        convert_button = driver.find_element(By.XPATH, '//span[text()="Chuyển đổi link"]')
    except:
        convert_button = driver.find_element(By.XPATH, '//span[text()="Link Convertor"]')
    convert_button.click()
    time.sleep(2)

    # Nhập link cần chuyển đổi
    try:
        link_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Dán link tại đây"]')
    except:
        link_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Paste page url here"]')
    link_input.send_keys(link_to_convert)

    # Nhấn nút "Confirm Convert"
    confirm_button = driver.find_element(By.CLASS_NAME, 'link-convert-confirm')
    confirm_button.click()
    time.sleep(3)  # Đợi chuyển đổi hoàn tất

    # Lấy link đã chuyển đổi
    success_message = driver.find_element(By.CLASS_NAME, 'copy-link-successful-title')
    converted_link = success_message.find_elements(By.TAG_NAME, 'div')[1].text
    print(f"Link đã chuyển đổi: {converted_link}")

    # Nhấn nút "Copy" để sao chép link trong pop-up thành công
    try:
        copy_button = driver.find_element(By.CLASS_NAME, 'copy-link-copy-btn')
        copy_button.click()
        print("Đã nhấn nút Copy thành công.")
    except:
        print("Không thể nhấn nút Copy.")

    # Đóng pop-up "Link Convertor" để chuẩn bị sẵn sàng cho lần chuyển đổi tiếp theo
    try:
        close_button = driver.find_element(By.CLASS_NAME, 'next-dialog-close')
        close_button.click()
        print("Đã đóng pop-up 'Link Convertor' thành công.")
    except:
        print("Không thể đóng pop-up 'Link Convertor'.")

    return converted_link

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Đăng nhập và lưu trạng thái
        if login_to_lazada(username, password):
            session['logged_in'] = True
            return redirect(url_for('process'))
        else:
            return "Login failed. Please try again."

    return render_template('login.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        link = request.form['link']
        converted_link = convert_link(link)
        return render_template('process.html', converted_link=converted_link)

    return render_template('process.html', converted_link=None)

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
