import pyperclip  # Thêm thư viện này để hỗ trợ sao chép vào clipboard
import time
from selenium.webdriver.common.by import By

# Hàm convert_link được tối giản để sử dụng driver hiện có từ app.py
def convert_link(link_to_convert):
    global driver
    # Tìm form nhập link và dán link cần chuyển đổi
    try:
        link_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Dán link tại đây"]')
    except:
        link_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Paste page url here"]')

    # Dán link cần chuyển đổi
    link_input.send_keys(link_to_convert)

    # Nhấn nút "Chuyển đổi" hoặc "Confirm Convert"
    try:
        confirm_button = driver.find_element(By.XPATH, '//button[contains(text(),"Chuyển đổi") or contains(text(),"Confirm Convert")]')
    except:
        print("Không tìm thấy nút 'Chuyển đổi' hoặc 'Confirm Convert'")
        return None

    confirm_button.click()
    time.sleep(3)  # Đợi chuyển đổi hoàn tất

    # Lấy link đã chuyển đổi thành công
    try:
        success_message = driver.find_element(By.CLASS_NAME, 'copy-link-successful-title')
        converted_link = success_message.find_elements(By.TAG_NAME, 'div')[1].text
        print(f"Link đã chuyển đổi: {converted_link}")

        # Sao chép link vào clipboard
        pyperclip.copy(converted_link)
        print("Link đã được sao chép vào clipboard thành công!")

        # Đóng pop-up "Confirm Convert Successful"
        try:
            copy_button = driver.find_element(By.CLASS_NAME, 'copy-link-copy-btn')
            copy_button.click()
        except:
            try:
                cancel_button = driver.find_element(By.CLASS_NAME, 'copy-link-cancel-btn')
                cancel_button.click()
            except:
                print("Không thể nhấn nút Copy hoặc Cancel")

        # Kiểm tra và tắt nút Close
        time.sleep(1)
        close_buttons = driver.find_elements(By.CLASS_NAME, 'next-dialog-close-icon')
        for button in close_buttons:
            try:
                button.click()
                print("Đã đóng pop-up thành công.")
            except:
                print("Không thể đóng pop-up.")

    except:
        print("Không tìm thấy phần tử thành công chuyển đổi")
        return None

    return converted_link