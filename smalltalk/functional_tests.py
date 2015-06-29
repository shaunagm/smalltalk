from selenium import webdriver
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
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention 'Smalltalk'
        self.assertIn('Smalltalk', self.browser.title)
        self.assertIn('Smalltalk',
            self.browser.find_element_by_id('header-title').text)

        # She sees a button labeled 'Create New Contact'.
        self.assertIn('New Contact',
            self.browser.find_element_by_id('new_contact_button').text)

        # She clicks it and a new contact form appears
        self.assertEqual(False,
            self.browser.find_element_by_id('contact_form_container').is_displayed())
        self.browser.find_element_by_id('new_contact_button').click()
        self.assertIn('Name',
            self.browser.find_element_by_id('contact_form_container').text)

        # She clicks submit without filling out the form, and the form gives her
        # an error message reminding her to fill out the required fields.

        # She fills out the required fields and is taken to view her new contact.

        # She decides she wants to add additional information to the contact, so
        # she clicks the "edit" button.

        # Once she saves her changes, the new contact view is updated.

        # She decides to add her new contact to a group, so she clicks the
        # "Add to Group(s)" button.  She can now see a checklist of existing
        # groups.

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
