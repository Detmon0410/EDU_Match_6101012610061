from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, unittest
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
'''
    def test_user_can_join_home_page(self):
        # Mok has trouble learning. So he went to see the home page
        # of the website that his friend introduced
        self.browser.get(self.live_server_url)

        # He saw that the title of this website is EDU-Match Login
        self.assertIn('Login', self.browser.title)
        # saw login box on this page
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Login', header_text)
        time.sleep(5)




    def test_can_user_register_login_and_edit_profile(self):
        # he going to register
        self.browser.get(self.live_server_url + '/signup')

        # he saw title as Sign Up
        self.assertIn('Sign Up', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Sign Up', header_text)

        # he type username as somsak
        input_username = self.browser.find_element_by_id('id_username')
        input_username.send_keys('somsak')

        # he type firestname and lastname as Pasakorn Phareyart
        input_firstname = self.browser.find_element_by_id('id_first_name')
        input_firstname.send_keys('Paskorn')
        input_lastname = self.browser.find_element_by_id('id_last_name')
        input_lastname.send_keys('Phareyart')

        # he set email as example@gmail.com
        input_email = self.browser.find_element_by_id('id_email')
        input_email.send_keys('example@gmail.com')

        # he type password as mok123456789
        input_password = self.browser.find_element_by_id('id_password1')
        input_password.send_keys('mok123456789')
        # he confirm password
        input_password_seconds = self.browser.find_element_by_id('id_password2')
        input_password_seconds.send_keys('mok123456789')
        time.sleep(3)
        # He press Enter
        input_password_seconds.send_keys(Keys.ENTER)
        time.sleep(3)

        # Next he saw login page
        self.assertIn('Login', self.browser.title)

        # he type user name
        input_username_login = self.browser.find_element_by_id('id_username')
        input_username_login.send_keys('somsak')

        # he type pass word
        input_password = self.browser.find_element_by_id('id_password')
        input_password.send_keys('mok123456789')
        time.sleep(3)
        # He press Enter
        input_password.send_keys(Keys.ENTER)
        time.sleep(3)

        # he saw his name was wrong form Pasakorn to Paskorn
        name_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Paskorn', name_text)

        # he click his profile button
        text_profile = self.browser.find_element_by_id('id_profile')
        text_profile.send_keys(Keys.ENTER)
        time.sleep(3)

        self.assertIn('Profile', self.browser.title)
        time.sleep(3)
        # he saw wrong name in textinput
        input_first_name_profile = self.browser.find_element_by_id('id_first_name')
        self.assertIn('Paskorn', input_first_name_profile.get_attribute("value"))

        # now he type true name as Pasakorn
        input_first_name_profile.clear()
        input_first_name_profile.send_keys('Pasakorn')
        time.sleep(3)
        # he press Enter
        input_first_name_profile.send_keys(Keys.ENTER)
        time.sleep(3)

        # now his name is Pasakorn
        name_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Pasakorn', name_text)
        time.sleep(3)
        # he want to change pass word
        self.sup_test_can_user_change_password()




    def sup_test_can_user_change_password(self):
        # and then he want to change pass word
        # he going to change pass word page
        self.browser.get(self.live_server_url + '/accounts/change_password/')
        time.sleep(3)

        # he saw head text as Change Password
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Change Password', header_text)

        # he type  Old password
        old_password = self.browser.find_element_by_id('id_old_password')
        old_password.send_keys('mok123456789')

        # he type new pass word
        new_password_a = self.browser.find_element_by_id('id_new_password1')
        new_password_a.send_keys('mok987654321')

        # he confirm new pass word
        new_password_b = self.browser.find_element_by_id('id_new_password2')
        new_password_b.send_keys('mok987654321')
        time.sleep(3)
        # he press Enter
        new_password_b.send_keys(Keys.ENTER)
        time.sleep(3)

        # he saw notification Password changed with success
        success_text = self.browser.find_element_by_tag_name('p').text
        self.assertIn('Password changed with success!!!', success_text)

        # he going to logout
        # he login agian
        link_logout = self.browser.find_element_by_id('id_logout')
        link_logout.send_keys(Keys.ENTER)
        time.sleep(3)

        # he saw login title
        self.assertIn('Login', self.browser.title)

        # he type username
        input_username_login = self.browser.find_element_by_id('id_username')
        input_username_login.send_keys('somsak')

        # he type pass word as mok987654321
        input_password = self.browser.find_element_by_id('id_password')
        input_password.send_keys('mok987654321')
        time.sleep(3)
        # จากนั้นเขาจึงกดปุ่ม Enter
        input_password.send_keys(Keys.ENTER)
        time.sleep(3)

        # he saw homepage title
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to EDU-Match', header_text)

        time.sleep(3)





    def test_add_subject_and_user_search_for_matching(self):
        self.browser.get(self.live_server_url + '/signup')

        # jack join Match-EDU signup page
        time.sleep(3)
        self.assertIn('Sign Up', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h2').text
        # he check title of page was Sign Up
        self.assertIn('Sign Up', header_text)

        # he type username as jackel1234
        input_username = self.browser.find_element_by_id('id_username')
        input_username.send_keys('jackel1234')

        # he type his 1st name and last name
        input_firstname = self.browser.find_element_by_id('id_first_name')
        input_firstname.send_keys('Jake')
        input_lastname = self.browser.find_element_by_id('id_last_name')
        input_lastname.send_keys('Kelvin')

        # he type email
        input_email = self.browser.find_element_by_id('id_email')
        input_email.send_keys('jake@gmail.com')

        # he type password
        input_password = self.browser.find_element_by_id('id_password1')
        input_password.send_keys('jk123456')
        # he confirm that password
        input_password_seconds = self.browser.find_element_by_id('id_password2')
        input_password_seconds.send_keys('jk123456')
        time.sleep(3)
        # he press Enter
        input_password_seconds.send_keys(Keys.ENTER)
        time.sleep(3)

        # he going to login page and check title o fpage
        self.assertIn('Login', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Login', header_text)

        # he type user name
        username_login = self.browser.find_element_by_id('id_username')
        username_login.send_keys('jackel1234')

        # he type pass word
        password_login = self.browser.find_element_by_id('id_password')
        password_login.send_keys('jk123456')

        # จากนั้นเขาจึงกดปุ่ม Enter
        password_login.send_keys(Keys.ENTER)
        time.sleep(5)

        # he join to home page
        self.browser.get(self.live_server_url)
        self.assertIn('EDU-MATCH', self.browser.title)

        # he saw welcome text
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to EDU-Match, Hello Jake !', header_text)

        # he going to add expert subject page
        self.browser.get(self.live_server_url + '/profile_add_subject')
        input_box = self.browser.find_element_by_id('id_new_subject')
        self.assertIn(
            input_box.get_attribute('placeholder'),
            'Enter a expert Subject'
        )
        # He typed "English 1"
        input_box.send_keys('English 1')
        time.sleep(3)
        # he click add subject
        input_box.send_keys(Keys.ENTER)
        time.sleep(5)

        # he saw his English 1 subject
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('english1', [row.text for row in rows])
        time.sleep(5)

        # Next Detmon join sign up page
        self.browser.get(self.live_server_url + '/signup')

        # he saw title of page
        self.assertIn('Sign Up', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Sign Up', header_text)

        # he type username as detmonmok
        input_username = self.browser.find_element_by_id('id_username')
        input_username.send_keys('detmonmok')

        # he type 1st name and last name
        input_firstname = self.browser.find_element_by_id('id_first_name')
        input_firstname.send_keys('Detmon')
        input_lastname = self.browser.find_element_by_id('id_last_name')
        input_lastname.send_keys('Jangit')

        # he type email
        input_email = self.browser.find_element_by_id('id_email')
        input_email.send_keys('detmon@gmail.com')

        # he set pass word as mok123456789
        input_password = self.browser.find_element_by_id('id_password1')
        input_password.send_keys('mok123456789')
        # he confirm pass word
        input_password_seconds = self.browser.find_element_by_id('id_password2')
        input_password_seconds.send_keys('mok123456789')

        # he press Enter
        input_password_seconds.send_keys(Keys.ENTER)
        time.sleep(5)


        # he going to login
        # he type user name
        username_login = self.browser.find_element_by_id('id_username')
        username_login.send_keys('detmonmok')

        # he type password Mokza007
        password_login = self.browser.find_element_by_id('id_password')
        password_login.send_keys('mok123456789')

        # he press Enter
        password_login.send_keys(Keys.ENTER)
        time.sleep(1)

        # From then, he added the names of subjects that he was not good at anymore
        self.browser.get(self.live_server_url)
        self.assertIn('EDU-MATCH', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome to EDU-Match, Hello Detmon !', header_text)

        input_box = self.browser.find_element_by_id('id_new_subject')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a Subject'
        )
        # He typed "English 1"
        input_box.send_keys('English 1')
        input_box.send_keys(Keys.ENTER)
        # web will display user was expert with this subject
        time.sleep(5)
        self.sup_test_to_review()





    def sup_test_to_review(self):
        self.browser.get(self.live_server_url + '/friendprofile/jackel1234')
        time.sleep(5)
        


        input_box = self.browser.find_element_by_id('id_review')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Write Your Message Here'
        )
        input_box.send_keys("He is a nice person and good at teaching")
        time.sleep(3)
        press_review=self.browser.find_element_by_id('review_button')
        press_review.send_keys(Keys.ENTER)
        time.sleep(5)'''




class ChattingTest(unittest.TestCase):
    def setUp(self):
        self.browser_firefox = webdriver.Firefox()
        self.browser_chrome = webdriver.Chrome()

    def tearDown(self):
        self.browser_firefox.quit()
        self.browser_chrome.quit()

    def test_user_can_chatting(self):
        # Mr.beta login to EDU-Match for chatting
        self.browser_firefox.get('http://127.0.0.1:8000/accounts/login/')
        self.assertIn('Login', self.browser_firefox.title)
        input_username_login_user_a = self.browser_firefox.find_element_by_id('id_username')
        input_username_login_user_a.send_keys('alpha04')
        input_password_user_a = self.browser_firefox.find_element_by_id('id_password')
        input_password_user_a.send_keys('ap123456')
        input_password_user_a.send_keys(Keys.ENTER)
        time.sleep(2)
        # He going to chat room for chat with alpha tutor

        self.browser_firefox.get('http://127.0.0.1:8000/chat/testroom09/')
        #self.browser1.get('http://127.0.0.1:8000/chat/alpha04beta02/')
        time.sleep(2)

        # MR.beta login to EDU-Match for chatting
        self.browser_chrome.get('http://127.0.0.1:8000/accounts/login/')
        self.assertIn('Login', self.browser_chrome.title)
        input_username_login_user2 = self.browser_chrome.find_element_by_id('id_username')
        input_username_login_user2.send_keys('beta02')
        input_password_user2 = self.browser_chrome.find_element_by_id('id_password')
        input_password_user2.send_keys('bt123456')
        time.sleep(3)
        input_password_user2.send_keys(Keys.ENTER)
        time.sleep(3)
        # Mr.beta going to chat room for chat with alpha student
        self.browser_chrome.get('http://127.0.0.1:8000/chat/testroom09/')
        #self.browser2.get('http://127.0.0.1:8000/chat/alpha04beta02/')
        time.sleep(2)

        # Mr.beta and alpha See the chat log
        chat_box_firefox = self.browser_firefox.find_element_by_id('chat-log')
        chat_box_chrome = self.browser_chrome.find_element_by_id('chat-log')

        # # Mr.beta and alpha See the chat  textbox
        chat_textbox_firefox = self.browser_firefox.find_element_by_id('chat-message-input')
        self.assertIn(
            chat_textbox_firefox.get_attribute('type'),
            'text'
        )
        chat_textbox_chrome = self.browser_chrome.find_element_by_id('chat-message-input')
        self.assertIn(
            chat_textbox_chrome.get_attribute('type'),
            'text'
        )



        # alpha types message "hello"
        chat_textbox_chrome.send_keys('hello')
        time.sleep(2)

        # alpha clicks the send button.
        chat_textbox_chrome.send_keys(Keys.ENTER)
        time.sleep(2)

        # alpha notices his message is send in textarea
        self.assertIn(
            chat_box_chrome.get_attribute('value'),
            '\t\t\t\t\t\t\t\t\t\t\t\t\t\tbeta02 :hello\n'
        )

        # alpha types message "Hi"
        chat_textbox_chrome.send_keys('How are you? ')
        time.sleep(2)

        # alpha clicks the send button.
        chat_textbox_chrome.send_keys(Keys.ENTER)
        time.sleep(2)

        # beta notices his message is send in textarea
        self.assertIn(
            chat_box_chrome.get_attribute('value'),
            '\t\t\t\t\t\t\t\t\t\t\t\t\t\tbeta02 :hello\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tbeta02 :How are you? \n'

        )



        # Mr.beta notices Alpha message  in textarea
        self.assertIn(
            chat_box_firefox.get_attribute('value'),
            'beta02 :hello\nbeta02 :How are you? \n'
        )

        # alpha types message "i'm fine"
        chat_textbox_firefox.send_keys('im fine')
        time.sleep(2)

        # alpha clicks the send button.
        chat_textbox_firefox.send_keys(Keys.ENTER)
        time.sleep(2)

        # alpha notices his message is send in textarea
        self.assertIn(
            chat_box_firefox.get_attribute('value'),
            'beta02 :hello\nbeta02 :How are you? \n\t\t\t\t\t\t\t\t\t\t\t\t\t\talpha04 :im fine\n'
        )



        time.sleep(3)
