from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_a_contact(self):
        # Buffy has heard about a cool new online app.  She goes to check out
        # its homepage
        self.browser.get('http://127.0.0.1:8000')

        # She notices the page title says 'Smalltalk' and the text of the page
        # includes "Welcome!"
        self.assertIn('Smalltalk', self.browser.title)
        self.assertIn('Welcome!',
            self.browser.find_element_by_css_selector('h2').text)

        # She sees a prompt to create a new contact.  She clicks it and is brought
        # to a new page with a contact creation form.
        self.assertIn('New Contact',
            self.browser.find_element_by_id('nav_new_contact').get_attribute('innerHTML'))
        self.browser.find_element_by_id('contact_dropdown_toggle').click()
        self.browser.find_element_by_id('nav_new_contact').click()
        self.assertIn('contact/new', self.browser.current_url)
        self.assertTrue(self.browser.find_element_by_id('edit_contact_submit'))

        # She clicks submit without filling out the form, and the form gives her
        # an error message reminding her to fill out the required fields.
        self.assertEqual("",
            self.browser.find_element_by_id('new_contact_message').text)
        self.browser.find_element_by_id('edit_contact_submit').click()
        self.assertIn("The name field is required.",
            self.browser.find_element_by_class_name('errorlist').text)

        # She fills out the required fields and is taken to a new page where she can
        # see the contact details.
        name_input = self.browser.find_element_by_id('id_name')
        name_input.send_keys("Willow Rosenberg")
        self.browser.find_element_by_id('edit_contact_submit').click()
        self.assertIn("Contact Details", self.browser.title)

        # She decides she wants to add additional information to the contact, so
        # she clicks the "edit" button.
        self.browser.find_element_by_id('contact_edit').click()
        self.assertIn("Edit", self.browser.title)

        # There, she adds some information to the details field.
        details_input = self.browser.find_element_by_id('id_details')
        details_input.send_keys("Hacker, witch, and bff")

        # Once she saves her changes, the new contact view is updated.
        self.browser.find_element_by_id('edit_contact_submit').click()
        self.assertIn("Hacker, witch, and bff",
            self.browser.find_element_by_id('contact_details').text)

        # She decides to add her new contact to a group, so she clicks the
        # "Add to Group(s)" button.  She is informed that she needs to create
        # groups before she can add contacts to them.
        self.browser.find_element_by_id('add_to_group').click()
        time.sleep(.5)
        self.assertIn("You do not have any groups.",
            self.browser.find_element_by_id('group_message').get_attribute('innerHTML'))

        # She clicks the "Create a group" link and is brought to a new page with
        # a form to create a new group.
        self.browser.find_element_by_id('contact_dropdown_toggle').click()
        self.browser.find_element_by_id('nav_new_group').click()
        self.assertIn("Edit", self.browser.title)
        self.assertIn('group/new', self.browser.current_url)
        self.assertTrue(self.browser.find_element_by_id('edit_group_submit'))

        # She selects one of the existing groups and clicks 'save'. The contact
        # view now displays that the contact is in a group.

        self.fail('Finish the test!')

    # def test_can_add_a_topic(self):

    # def test_can_create_an_account(self):

        # She sees that the page prompts her to create an account to use the app.

        # She clicks the 'create account' button and is prompted for a user name
        # & password.



if __name__ == '__main__':
    unittest.main(warnings='ignore')
