from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, unittest
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_edu_match_and_retrieve_it_later(self):
        # Mok has trouble learning. So he went to see the home page
        # of the website that his friend introduced
        self.browser.get(self.live_server_url)

        # He saw that the title of this website is EDU-Match
        self.assertIn('EDU-MATCH', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to EDU-Match', header_text)

        inputbox = self.browser.find_element_by_id('id_new_subject')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a Subject'
        )

        # He type the name of the subject that was not good
        # He type "Statistics in everyday life" into the Text box
        inputbox.send_keys('Statistics in everyday life')

        # When he press Enter, the page shows the name of a person who is good at "Statistics in everyday life"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # table = self.browser.find_element_by_id('id_list_matching')
        # rows = table.find_elements_by_tag_name('tr')

        # She visits that URL - her to-do list is still there.
        self.fail('Finish the test!')

    def test_can_user_register_login_and_edit_profile(self):
        # ตอนนี้ หมอกยังไม่ได้เป็นสมาชิก
        # ดังนั้น เขาจึงสมัครสมาชิก
        self.browser.get(self.live_server_url + '/signup')
        # เขาเห็นว่า title มีชื่อว่า Sign Up
        # ซึ่งเเสดงว่าเขาเข้ามาถูก
        self.assertIn('Sign Up', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Sign up into Website', header_text)

        # เขาจึงใส่ username เป็น somsak
        inputusername = self.browser.find_element_by_id('id_username')
        inputusername.send_keys('somsak')

        # เขาได้ใส่ชื่อเเละนามสกุลเป็น Pasakorn Phareyart เเต่เขาใส่ชื่อผิด จึงเป็น Paskorn
        input_firstname = self.browser.find_element_by_id('id_first_name')
        input_firstname.send_keys('Paskorn')
        input_lastname = self.browser.find_element_by_id('id_last_name')
        input_lastname.send_keys('Phareyart')

        # เขาได้ใส่ E-mail เป็น example@gmail.com
        input_email = self.browser.find_element_by_id('id_email')
        input_email.send_keys('example@gmail.com')

        # ต่อมาเขาใส่รหัสเป็น mok123456789
        inputpassword = self.browser.find_element_by_id('id_password1')
        inputpassword.send_keys('mok123456789')
        inputpassword2 = self.browser.find_element_by_id('id_password2')
        inputpassword2.send_keys('mok123456789')

        # เขาจึงกดปุ่ม Enter
        inputpassword2.send_keys(Keys.ENTER)
        time.sleep(1)

        # เมื่อเขาสมัครสมาชิกเสร็จเเล้ว
        # เขาจึงไปที่หน้า login
        self.assertIn('Login', self.browser.title)

        # เขาพิมพ์ Username เเละ password ลงไป
        # เขาจึงใส่ username เป็น somsak
        inputusername_login = self.browser.find_element_by_id('id_username')
        inputusername_login.send_keys('somsak')

        # ต่อมาเขาใส่รหัสเป็น mok123456789
        inputpassword = self.browser.find_element_by_id('id_password')
        inputpassword.send_keys('mok123456789')

        # จากนั้นเขาจึงกดปุ่ม Enter
        inputpassword.send_keys(Keys.ENTER)
        time.sleep(3)

        # เขาสังเกตเห็นว่าชื่อที่ปรากฏผิดจาก Pasakorn เป็น Paskorn
        name_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Paskorn', name_text)

        # เขาจึงเข้าไปที่หน้า Profile เพื่อแก้ไข
        text_profile = self.browser.find_element_by_id('id_profile')
        text_profile.send_keys(Keys.ENTER)
        time.sleep(1)

        self.assertIn('Profile', self.browser.title)

        # เขาเห็นชื่อที่ผิดรากฏอยู่ที่ textinput
        input_firstname_profile = self.browser.find_element_by_id('id_first_name')
        # print(input_firstname_profile)
        self.assertIn('Paskorn', input_firstname_profile.get_attribute("value"))

        # เขาจึงลบชื่อที่ผิดเเละเเก้เป็น Pasakorn
        input_firstname_profile.clear()
        input_firstname_profile.send_keys('Pasakorn')

        # จากนั้นเขาก็กด Enter
        input_firstname_profile.send_keys(Keys.ENTER)
        time.sleep(1)

        # เขาสังเกตเห็นว่าชื่อที่ปรากฏเป็น Pasakorn ซึ่งเป็นชื่อที่เขาต้องการ
        name_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Pasakorn', name_text)

        self.test_can_user_change_password()

        # หลังจากที่เขาเล่นเว็บ EDU-Match เสร็จเเล้ว
        # เขาจึงกดไปที่ Log out
        self.fail('Finish the test!')

    def test_can_user_change_password(self):
        # หลังจากที่เข้าสมัครเเละเปลียนชื่อเรียบร้อยเเล้ว
        # เขาจีงต้องการที่จะเปลี่ยนรหัสของเขา
        # เขาจึงเข้ามาที่หน้าเปลี่ยนรหัส
        self.browser.get(self.live_server_url + '/accounts/change_password/')
        time.sleep(1)

        # จากนั้นเห็นอีกว่าหัวข้อของหน้านี้คือ Change Password
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Change Password', header_text)

        # เมื่อเขาเข้ามาที่หน้านี้ เขาจึงใส่รหัสเก่าของเขาที่ช่อง Old password
        old_password = self.browser.find_element_by_id('id_old_password')
        old_password.send_keys('mok123456789')

        # จากนั้นเขาก็ใส่รหัสใหม่ของเขาคือ mok987654321
        new_password1 = self.browser.find_element_by_id('id_new_password1')
        new_password1.send_keys('mok987654321')

        # เเละยืนยันรหัสอีก 1 รอบ
        new_password2 = self.browser.find_element_by_id('id_new_password2')
        new_password2.send_keys('mok987654321')

        # เเละกดปุ่ม Enter
        new_password2.send_keys(Keys.ENTER)
        time.sleep(1)

        # เขาสังเกตเห็นคำว่า Password changed with success
        success_text = self.browser.find_element_by_tag_name('p').text
        self.assertIn('Password changed with success!!!', success_text)

        # เเละเห็นคำว่า Logout ที่มันสามารถกดได้
        # เขาจึงกดคำนั้นเพื่อ Login ใหม่อีกครั้ง
        link_logout = self.browser.find_element_by_id('id_logout')
        link_logout.send_keys(Keys.ENTER)
        time.sleep(1)

        # เขามาที่หน้า Login เเล้ว เขาจึงใส่รหัสใหม่ทันที
        self.assertIn('Login', self.browser.title)

        # เขาพิมพ์ Username เเละ password ลงไป
        # เขาจึงใส่ username เป็น somsak
        inputusername_login = self.browser.find_element_by_id('id_username')
        inputusername_login.send_keys('somsak')

        # ต่อมาเขาใส่รหัสเป็น mok987654321
        inputpassword = self.browser.find_element_by_id('id_password')
        inputpassword.send_keys('mok987654321')

        # จากนั้นเขาจึงกดปุ่ม Enter
        inputpassword.send_keys(Keys.ENTER)
        time.sleep(1)

        # เเละในที่สุดรหัสของเขาก็ได้ถูกเปลี่ยนไปเเล้ว
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to EDU-Match', header_text)

        self.fail('Finish the test!')

    def test_to_search_for_matching(self):
        self.browser.get(self.live_server_url + '/signup')
        # เขาเห็นว่า title มีชื่อว่า Sign Up
        # ซึ่งเเสดงว่าเขาเข้ามาถูก
        self.assertIn('Sign Up', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Sign up into Website', header_text)

        # เขาจึงใส่ username เป็น detmonmok
        inputusername = self.browser.find_element_by_id('id_username')
        inputusername.send_keys('detmonmok')

        # ต่อมาเขาใส่รหัสเป็น mok123456789
        inputpassword = self.browser.find_element_by_id('id_password1')
        inputpassword.send_keys('mok123456789')
        inputpassword2 = self.browser.find_element_by_id('id_password2')
        inputpassword2.send_keys('mok123456789')

        # เขาจึงกดปุ่ม Enter
        inputpassword2.send_keys(Keys.ENTER)
        time.sleep(1)

        self.browser.get(self.live_server_url + '/account/login/')

        # เขาพิมพ์ Username เเละ password ลงไป
        # เขาจึงใส่ username เป็น moklnwza
        inputusername = self.browser.find_element_by_id('id_username')
        inputusername.send_keys('detmonmok')

        # ต่อมาเขาใส่รหัสเป็น Mokza007
        inputpassword = self.browser.find_element_by_id('id_password')
        inputpassword.send_keys('mok123456789')

        # จากนั้นเขาจึงกดปุ่ม Enter
        inputpassword.send_keys(Keys.ENTER)
        time.sleep(1)

        # From then, he added the names of subjects that he was not good at anymore
        self.browser.get(self.live_server_url)
        self.assertIn('EDU-MATCH', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to My Site , Hello Pasakorn !', header_text)

        inputbox = self.browser.find_element_by_id('id_new_subject')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a Subject'
        )
        # He typed "General Mathematics"
        inputbox.send_keys('General Mathematics')

        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The webpage shows more people who specialize in "General Mathematics"
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1:kitsanapong', [row.text for row in rows])
        # Later, he wanted to know what would happen if he typed a subject that didn't exist
        inputbox.send_keys('Nothing')

        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The webpage shows the message "No match found. Ready to match. Please re-match later."
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('No users were found matching', [row.text for row in rows])
        self.fail('Finish the test!')
    # He takes the time to choose someone to tutor for a long time

    # He feels like this website very much


def test_to_review(self):
    self.browser.get(self.live_server_url + '/signup')
    # เขาเห็นว่า title มีชื่อว่า Sign Up
    # ซึ่งเเสดงว่าเขาเข้ามาถูก
    self.assertIn('Sign Up', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h2').text
    self.assertIn('Sign up into Website', header_text)

    # เขาจึงใส่ username เป็น detmonmok
    inputusername = self.browser.find_element_by_id('id_username')
    inputusername.send_keys('detmonohm')

    # ต่อมาเขาใส่รหัสเป็น mok123456789
    inputpassword = self.browser.find_element_by_id('id_password1')
    inputpassword.send_keys('ohm123456789')
    inputpassword2 = self.browser.find_element_by_id('id_password2')
    inputpassword2.send_keys('ohm123456789')

    # เขาจึงกดปุ่ม Enter
    inputpassword2.send_keys(Keys.ENTER)
    time.sleep(1)

    self.browser.get(self.live_server_url + '/account/login/')

    # เขาพิมพ์ Username เเละ password ลงไป
    # เขาจึงใส่ username เป็น moklnwza
    inputusername = self.browser.find_element_by_id('id_username')
    inputusername.send_keys('detmonohm')

    # ต่อมาเขาใส่รหัสเป็น Mokza007
    inputpassword = self.browser.find_element_by_id('id_password')
    inputpassword.send_keys('ohm123456789')

    # จากนั้นเขาจึงกดปุ่ม Enter
    inputpassword.send_keys(Keys.ENTER)
    time.sleep(1)

    # From then, he added the names of subjects that he was not good at anymore

    self.browser.get(self.live_server_url + '/view_profile/kitsanapong')
    header_text = self.browser.find_element_by_tag_name('h3').text
    self.assertIn('Review', header_text)
    sub_header_text = self.browser.find_element_by_tag_name('h3').text
    self.assertIn('Leave a review', sub_header_text)
    inputbox = self.browser.find_element_by_id('id_review')
    self.assertEqual(
        inputbox.get_attribute('placeholder'),
        'Write Your Message Here'
    )
    inputbox.send_keys("He is a nice person and good at teaching")
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)
    table = self.browser.find_element_by_id('id_list_review')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn('detmonohm : He is a nice person and good at teaching', [row.text for row in rows])
    self.fail('Finish the test!')


#        # He click on Profile button
#         buttontoprofile = self.browser.find_element_by_id('id_to_profile')
#         buttontoprofile.send_keys(Keys.ENTER)
#         self.browser.get('http://localhost:8000/profile')
# He saw that the header of this website is My profile
#        pheader_text = self.browser.find_element_by_tag_name('h2').text
#        self.assertIn('My Profile', pheader_text)
# He type his favorite subject
# He type "Math2" and "Biology" into the Text box
#        inputbox = self.browser.find_element_by_id('id_new_subject')
#        inputbox.send_keys('Math2')
#        inputbox.send_keys(Keys.ENTER)
#        time.sleep(1)
#        inputbox = self.browser.find_element_by_id('id_new_subject')
#        inputbox.send_keys('Biology')
#        inputbox.send_keys(Keys.ENTER)
#        time.sleep(1)

# The page shows both subject on his list
#        table = self.browser.find_element_by_id('id_list_table')
#        rows = table.find_elements_by_tag_name('tr')
#        self.assertIn('1: Math2', [row.text for row in rows])
#        self.assertIn(
#            '2: Biology',
#             [row.text for row in rows]
#        )
# He select Biology and Math2 subject for remove and press remove
#        checkbox1 = self.browser.find_element_by_id('new_subject1')
#        checkbox1.send_keys(Keys.SPACE)
#        checkbox2 = self.browser.find_element_by_id('new_subject2')
#        checkbox2.send_keys(Keys.SPACE)
#        deletebutton = self.browser.find_element_by_id('id_delete_subject')
#        deletebutton.send_keys(Keys.ENTER)

'''class ChattingTest(unittest.TestCase):
    def setUp(self):
        self.browser1 = webdriver.Firefox()
        self.browser2 = webdriver.Chrome()

    def tearDown(self):
        self.browser1.quit()
        self.browser2.quit()

    def test_user_can_chatting(self):
        # Somsak login to EDU-Match for chatting
        self.browser1.get('http://127.0.0.1:8000/accounts/login/')
        self.assertIn('Login', self.browser1.title)
        inputusername_login_user1 = self.browser1.find_element_by_id('id_username')
        inputusername_login_user1.send_keys('somsak112')
        inputpassword_user1 = self.browser1.find_element_by_id('id_password')
        inputpassword_user1.send_keys('sm123456')
        inputpassword_user1.send_keys(Keys.ENTER)
        time.sleep(2)
        # He going to chat room for chat with Manop tutor

        self.browser1.get('http://127.0.0.1:8000/chat/Testroom8/')
        #self.browser1.get('http://127.0.0.1:8000/chat/somsak112manop_55/')
        time.sleep(2)

        # Manop login to EDU-Match for chatting
        self.browser2.get('http://127.0.0.1:8000/accounts/login/')
        self.assertIn('Login', self.browser2.title)
        inputusername_login_user2 = self.browser2.find_element_by_id('id_username')
        inputusername_login_user2.send_keys('manop_55')
        inputpassword_user2 = self.browser2.find_element_by_id('id_password')
        inputpassword_user2.send_keys('mn123456')
        time.sleep(3)
        inputpassword_user2.send_keys(Keys.ENTER)
        time.sleep(3)
        # Manop going to chat room for chat with Somsak student
        self.browser2.get('http://127.0.0.1:8000/chat/Testroom8/')
        #self.browser2.get('http://127.0.0.1:8000/chat/somsak112manop_55/')
        time.sleep(2)

        # Somsak and Manop See the chat log
        chatbox = self.browser1.find_element_by_id('chat-log')
        chatbox2 = self.browser2.find_element_by_id('chat-log')

        # # Somsak and Manop See the chat  textbox
        chat_textbox = self.browser1.find_element_by_id('chat-message-input')
        self.assertIn(
            chat_textbox.get_attribute('type'),
            'text'
        )
        chat_textbox2 = self.browser2.find_element_by_id('chat-message-input')
        self.assertIn(
            chat_textbox2.get_attribute('type'),
            'text'
        )

        # Manop and Somsak notices the send button
        send_button = self.browser1.find_element_by_id('chat-message-submit')
        self.assertIn(
            send_button.get_attribute('type'),
            'button'
        )
        send_button2 = self.browser2.find_element_by_id('chat-message-submit')
        self.assertIn(
            send_button2.get_attribute('type'),
            'button'
        )

        # Manop types message "hello"
        chat_textbox2.send_keys('hello')
        time.sleep(2)

        # Manop clicks the send button.
        send_button2.click()
        time.sleep(2)

        # Manop notices his message is send in textarea
        self.assertIn(
            chatbox2.get_attribute('value'),
            '\t\t\t\t\t\t\t\t\tmanop_55 :hello\n'
        )

        # Manop types message "Hi"
        chat_textbox2.send_keys('How are you? Somsak')
        time.sleep(2)

        # Manop clicks the send button.
        send_button2.click()
        time.sleep(2)

        # Manop notices his message is send in textarea
        self.assertIn(
            chatbox2.get_attribute('value'),
            '\t\t\t\t\t\t\t\t\tmanop_55 :hello\n\t\t\t\t\t\t\t\t\tmanop_55 :How are you? Somsak\n'

        )



        # Somsak notices manop message  in textarea
        self.assertIn(
            chatbox.get_attribute('value'),
            'manop_55 :hello\nmanop_55 :How are you? Somsak\n'
        )

        # somsak types message "i'm fine"
        chat_textbox.send_keys('im fine')
        time.sleep(2)

        # Manop clicks the send button.
        send_button.click()
        time.sleep(2)

        # somsak notices his message is send in textarea
        self.assertIn(
            chatbox.get_attribute('value'),
            'manop_55 :hello\nmanop_55 :How are you? Somsak\n\t\t\t\t\t\t\t\t\tsomsak112 :im fine\n'
        )



        time.sleep(3)'''
