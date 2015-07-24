import time
import unittest

from django.test import LiveServerTestCase
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class NewVisitorTest(LiveServerTestCase):

    def __init__(self, *args, **kwargs):
        super(NewVisitorTest, self).__init__(*args, **kwargs)
        if settings.DEBUG == False:
            settings.DEBUG = True

    def setUp(self):
        # Buffy has heard about a cool new online app.  She goes to check out
        # its homepage
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.get('%s' % (self.live_server_url))

        # She notices the page title says 'Smalltalk' and the text of the page
        # includes "Welcome!"
        self.assertIn('Smalltalk', self.browser.title)
        self.assertIn('Welcome!',
            self.browser.find_element_by_css_selector('h2').text)

    def tearDown(self):
        # Buffy's over it.
        self.browser.quit()

    def test_can_create_contacts(self):
        # Buffy sees a prompt to create a new contact.  She clicks it and is brought
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
        name_input = self.browser.find_element_by_id('id_shortname')
        name_input.send_keys("Willow Rosenberg")
        self.browser.find_element_by_id('edit_contact_submit').click()
        self.assertIn("Willow Rosenberg Contact Details", self.browser.title)

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
        self.browser.find_element_by_id('load_group_manager').click()
        time.sleep(.5)
        self.assertIn("You do not have any groups to add.",
            self.browser.find_element_by_id('group_list').text)

    def test_can_create_groups(self):
        # Buffy clicks the "Create a group" link and is brought to a new page with
        # a form to create a new group.
        self.browser.find_element_by_id('contact_dropdown_toggle').click()
        self.browser.find_element_by_id('nav_new_group').click()
        self.assertIn("Edit", self.browser.title)
        self.assertIn('group/new', self.browser.current_url)
        self.assertTrue(self.browser.find_element_by_id('edit_group_submit'))

        # She clicks submit without filling out the form, and the form gives her
        # an error message reminding her to fill out the required fields.
        self.assertEqual("",
            self.browser.find_element_by_id('new_group_message').text)
        self.browser.find_element_by_id('edit_group_submit').click()
        self.assertIn("The name field is required.",
            self.browser.find_element_by_class_name('errorlist').text)

        # She fills out the required fields and is taken to a new page where she can
        # see the contact details.
        name_input = self.browser.find_element_by_id('id_shortname')
        name_input.send_keys("Scoobies")
        self.browser.find_element_by_id('edit_group_submit').click()
        self.assertIn("Scoobies Group Details", self.browser.title)

        # She decides she wants to add additional information to the group, so
        # she clicks the "edit" button.
        self.browser.find_element_by_id('group_edit').click()
        self.assertIn("Edit", self.browser.title)

        # There, she adds some information to the details field.
        details_input = self.browser.find_element_by_id('id_details')
        details_input.send_keys("We laugh in the face of danger.")

        # Once she saves her changes, the new group view is updated.
        self.browser.find_element_by_id('edit_group_submit').click()
        self.assertIn("We laugh in the face of danger.",
            self.browser.find_element_by_id('group_details').text)

        # She decides to add a new contact to her group, so she clicks the
        # "Manage Contacts button.  She is informed that she needs to create
        # contacts before she can add groups to them.
        self.browser.find_element_by_id('load_contact_manager').click()
        time.sleep(.5)
        self.assertIn("You do not have any contacts to add.",
            self.browser.find_element_by_id('contact_list').text)

    def test_can_create_topics(self):
        # Buffy sees a prompt to create a new topic.  She clicks it and is brought
        # to a new page with a topic creation form.
        self.browser.find_element_by_id('topic_dropdown_toggle').click()
        self.browser.find_element_by_id('nav_new_topic').click()
        self.assertIn("Edit", self.browser.title)
        self.assertIn('topic/new', self.browser.current_url)
        self.assertTrue(self.browser.find_element_by_id('edit_topic_submit'))

        # She clicks submit without filling out the form, and the form gives her
        # an error message reminding her to fill out the required fields (details &
        # name this time).
        self.browser.find_element_by_id('edit_topic_submit').click()
        self.assertEqual("",
            self.browser.find_element_by_id('new_topic_message').text)
        self.browser.find_element_by_id('edit_topic_submit').click()
        self.assertIn("The name field is required.",
            self.browser.find_element_by_class_name('errorlist').text)

        # She fills out the other fields and is taken to a new page where she can
        # see the topic details.
        name_input = self.browser.find_element_by_id('id_shortname')
        name_input.send_keys("Selkies")
        self.browser.find_element_by_id('edit_topic_submit').click()
        self.assertIn("Selkies Topic Details", self.browser.title)

        # She decides she wants to add additional information to the topic, so
        # she clicks the "edit" button.
        self.browser.find_element_by_id('topic_edit').click()
        self.assertIn("Edit", self.browser.title)

        # There, she adds info to the details and links fields.
        details_input = self.browser.find_element_by_id('id_details')
        details_input.send_keys("Are they a thing?")
        link_input = self.browser.find_element_by_id('id_link')
        link_input.send_keys("https://en.wikipedia.org/wiki/Selkie")

        # Once she saves her changes, the new contact view is updated.
        self.browser.find_element_by_id('edit_topic_submit').click()
        self.assertIn("Are they a thing?",
            self.browser.find_element_by_id('topic_details').text)

        # self.fail('Finish the test!')

class ReturningVisitorTest(LiveServerTestCase):

    fixtures = ['test_fixtures']

    def __init__(self, *args, **kwargs):
        super(ReturningVisitorTest, self).__init__(*args, **kwargs)
        if settings.DEBUG == False:
            settings.DEBUG = True

    def setUp(self):
        # Buffy is returning to the website she found and added data to earlier.
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.get('%s' % (self.live_server_url))

    def tearDown(self):
        # Buffy's over it.
        self.browser.quit()

    def test_can_link_groups_to_contacts(self):
        # Buff now has groups and contacts.  She wants to start adding contacts
        # to her groups, so she goes to her lists of Contacts and selects Giles.
        self.browser.find_element_by_id('contact_dropdown_toggle').click()
        self.browser.find_element_by_id('nav_show_contacts').click()
        self.assertIn('contact/all', self.browser.current_url)
        self.browser.find_element_by_link_text('Giles').click()

        # Giles' page shows no groups listed, so she clicks the button labeled
        # "Manage Groups"  She is shown a short list of groups.
        self.assertIn("You have not added any groups yet.",
            self.browser.find_element_by_id('group_list').text)
        self.browser.find_element_by_id('load_group_manager').click()

        # She selects the group labelled "Scoobies" and clicks submit.  The page
        # now lists Giles as being in the "Scoobies" group.
        self.browser.find_element_by_id('id_groups_1').click()
        self.browser.find_element_by_id('manage_group_submit').click()
        time.sleep(.5)
        self.browser.find_element_by_link_text('Scoobies')

        # Buffy wonders if she can add contacts from the group page, so she
        # navigates to the 'Scoobies' group and clicks, "Manage Contacts".  She sees
        # a list of all of her contacts.
        self.browser.find_element_by_link_text('Scoobies').click()
        self.browser.find_element_by_id('load_contact_manager').click()
        self.assertEquals(6,
            len(self.browser.find_elements_by_name('contacts')))

        # Buffy selects Snyder and Cordelia and clicks submit.  The page now shows
        # Snyder, Giles, and Cordelia as part of the Scoobies.
        self.browser.find_element_by_id('id_contacts_0').click()
        self.browser.find_element_by_id('id_contacts_3').click()
        self.browser.find_element_by_id('manage_contact_submit').click()
        self.browser.find_element_by_link_text('Snyder')
        self.browser.find_element_by_link_text('Giles')
        self.browser.find_element_by_link_text('Cordelia')

        # Buffy closes the manage contacts form, and it disappears.
        self.browser.find_element_by_id('manage_contact_close').click()
        self.assertFalse(self.browser.find_element_by_id("inline_contact_div").is_displayed())

        # Buffy realizes that she doesn't want Snyder in the Scoobies group. She
        # selects "Manage Contacts" again.  She deselects Snyder and selects Giles,
        # and clicks submit.
        self.browser.find_element_by_id('load_contact_manager').click()
        self.browser.find_element_by_id('id_contacts_0').click()
        self.browser.find_element_by_id('manage_contact_submit').click()
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_link_text('Snyder')

    def test_can_link_topics_to_contacts_and_groups(self):
        # Buff now has groups and contacts.  She wants to add some topics to those
        # groups and contacts.  She starts by going to her list of Contacts and
        # selecting Giles.
        self.browser.find_element_by_id('contact_dropdown_toggle').click()
        self.browser.find_element_by_id('nav_show_contacts').click()
        self.assertIn('contact/all', self.browser.current_url)
        self.browser.find_element_by_link_text('Giles').click()

        # Giles' page shows no topics listed, so she clicks the button labelled
        # "Manage" next to "Topics".  She is shown a short list of topics.
        self.assertIn("You have not added any topics yet.",
            self.browser.find_element_by_id('topic_list').text)
        self.browser.find_element_by_id('load_topic_manager').click()

        # She selects the topic labelled "Apocalypse" and clicks submit.  The page
        # now lists Giles as having an Apocalypse topic.
        self.browser.find_element_by_id('id_topics_0').click()
        self.browser.find_element_by_id('manage_topic_submit').click()
        self.browser.find_element_by_link_text('Apocalypse')

        # Buffy wonders if she can add topics to groups as well, so she navigates
        # to the 'People' group and clicks on the button labelled "Manage" next to "Topics".
        self.browser.find_element_by_id('contact_dropdown_toggle').click()
        self.browser.find_element_by_id('nav_show_groups').click()
        self.browser.find_element_by_link_text('People').click()
        self.browser.find_element_by_id('load_topic_manager').click()

        # Buffy selects the topic labelled "The Bronze" and clicks submit.  The page
        # now lists the People group as having that topic.
        self.browser.find_element_by_id('id_topics_1').click()
        self.browser.find_element_by_id('manage_topic_submit').click()
        self.browser.find_element_by_link_text('The Bronze')

        # Buffy closes the manage topics form, and it disappears.
        self.browser.find_element_by_id('manage_topic_close').click()
        self.assertFalse(self.browser.find_element_by_id("inline_topic_div").is_displayed())

        # Buffy wonders if she can add groups and contacts directly from the topics
        # page.  She navigates to the 'Apocalypse' page and clicks "Manage Contacts".
        # She sees a list of all of her contacts.
        self.browser.find_element_by_id('topic_dropdown_toggle').click()
        self.browser.find_element_by_id('nav_show_topics').click()
        self.browser.find_element_by_link_text('Apocalypse').click()
        self.browser.find_element_by_id('load_contact_manager').click()
        self.assertEquals(6,
            len(self.browser.find_elements_by_name('contacts')))

        # Because of her previous actions, Giles is already associated with the topic.
        self.assertTrue(self.browser.find_element_by_id('id_contacts_1').is_selected())

        # # Buffy selects Cordelia and Spike and clicks submit.  The page
        # now shows Giles, Cordelia and Spike as being tagged with this topic.
        self.browser.find_element_by_id('id_contacts_2').click()
        self.browser.find_element_by_id('id_contacts_3').click()
        self.browser.find_element_by_id('manage_contact_submit').click()
        self.browser.find_element_by_link_text('Giles')
        self.browser.find_element_by_link_text('Spike')
        self.browser.find_element_by_link_text('Cordelia')

        # # Buffy realizes that she doesn't want Spike to know about the apocalypse,
        # so she selects "Manage Contacts" again.  She deselects Spike and clicks submit.
        # Now he is no longer listed.
        self.browser.find_element_by_id('load_contact_manager').click()
        self.browser.find_element_by_id('id_contacts_2').click()
        self.browser.find_element_by_id('manage_contact_submit').click()
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_link_text('Spike')

        # Next Buffy tries to add a group to the topic.  She closes the contact form
        # and opens the group form.
        self.browser.find_element_by_id('manage_contact_close').click()
        self.assertFalse(self.browser.find_element_by_id("inline_contact_div").is_displayed())
        self.browser.find_element_by_id('load_group_manager').click()
        self.assertTrue(self.browser.find_element_by_id("inline_group_div").is_displayed())

        # She selects the Scoobies group and clicks submit.  The page now shows the
        # Scoobies group as having this tag.
        self.browser.find_element_by_id('id_groups_1').click()
        self.browser.find_element_by_id('manage_group_submit').click()
        self.browser.find_element_by_link_text('Scoobies')

        # She clicks on the link to the Scoobies group.  Under topics, "Apocalypse"
        # is now listed.
        self.browser.find_element_by_link_text('Scoobies').click()
        self.browser.find_element_by_link_text('Apocalypse')

    # def test_can_add_topic_to_multiple_contacts_via_adding_to_group(self):
    #     # Buffy wants to be able to add a topic via the Scoobies tag but have it
    #     # show up on individual people's pages.  She starts by going to the Scoobies
    #     # group page and adding a topic.
    #     self.browser.find_element_by_id('contact_dropdown_toggle').click()
    #     self.browser.find_element_by_id('nav_show_groups').click()
    #     self.browser.find_element_by_link_text('Scoobies').click()
    #     self.browser.find_element_by_id('load_topic_manager').click()
    #     self.browser.find_element_by_id('id_topics_0').click()
    #     self.browser.find_element_by_id('manage_topic_submit').click()
    #     self.browser.find_element_by_link_text('Apocalypse')
    #
    #     # Next she checks the page for her friend Xander.  He does not have any
    #     # topics listed.
    #     self.browser.find_element_by_id('contact_dropdown_toggle').click()
    #     self.browser.find_element_by_id('nav_show_contacts').click()
    #     self.browser.find_element_by_link_text('Xander Harris').click()
    #     with self.assertRaises(NoSuchElementException):
    #         self.browser.find_element_by_link_text('Apocalypse')
    #
    #     # She returns to the Scoobies page and adds Xander to the group.
    #     self.browser.find_element_by_id('contact_dropdown_toggle').click()
    #     self.browser.find_element_by_id('nav_show_groups').click()
    #     self.browser.find_element_by_link_text('Scoobies').click()
    #     self.browser.find_element_by_id('load_contact_manager').click()
    #     self.browser.find_element_by_id('id_contacts_5').click()
    #     self.browser.find_element_by_id('manage_contact_submit').click()
    #     self.browser.find_element_by_link_text('Xander Harris')
    #
    #     # When she checks Xander's page again, a link to the topic shows up.
    #     self.browser.find_element_by_id('contact_dropdown_toggle').click()
    #     self.browser.find_element_by_id('nav_show_contacts').click()
    #     self.browser.find_element_by_link_text('Xander Harris').click()
    #     self.browser.find_element_by_link_text('Apocalypse')


    # def test_can_view_lists_of_info(self):

        # Buffy wants to see all of the information she's added.  She sees a navigation
        # link that says "show all topics" and clicks it.

        # Buffy is taken to a view with multiple topics listed.  When she selects the first
        # one, it takes her to a detail page.

        # Buffy returns to the main list view.  She sees that it is sorted by recency
        # by default.

        # Next, Buffy clicks on the "show all contacts" options.  She sees a list of contacts.

        # When she selects the first one, it takes her to a detail page.

        # Buffy returns to the main list view.  She sees that it is sorted by recency
        # by default.

        # Next, Buffy clicks on the "show all groups" options.  She sees a list of contacts.

        # When she selects the first one, it takes her to a detail page.

        # Buffy returns to the main list view.  She sees that it is sorted by recency
        # by default.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
