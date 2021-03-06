#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestDetailsPage:

    search_term = 'Wikipedia'

    @pytest.mark.nondestructive
    def test_that_application_page_contains_proper_objects(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search(self.search_term)

        # Select the first application link in the list
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        Assert.equal(details_page.app_name, self.search_term)

        # Check the application icon
        Assert.true(details_page.is_image_visible)

        # Check application title
        Assert.equal(details_page.name, details_page.app_name)

        # Check Application Developer username
        Assert.true(details_page.is_app_dev_username_visible)

        # Check the install/purchase button
        Assert.true(details_page.is_install_button_visible)

        # Check the application description
        Assert.true(details_page.is_application_description_visible)

        # Check the image preview section of the application
        Assert.true(details_page.is_image_preview_section_visible)

        # Check if the support email link is visible
        Assert.true(details_page.is_support_email_visible)

        #Check if support site or homepage link is visible
        Assert.true(details_page.is_app_site_visible)

        # Check if privacy policy link is visible
        Assert.true(details_page.is_privacy_policy_link_visible)

        # Check if report abuse button is visible
        Assert.true(details_page.is_report_abuse_button_visible)

    def test_that_reports_abuse_as_anonymous_user(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search(self.search_term)

        # Select the first application link in the list
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        Assert.true(details_page.is_report_abuse_button_visible)
        report_abuse_box = details_page.click_report_abuse_button()

        Assert.true(report_abuse_box.is_visible)
        Assert.false(report_abuse_box.is_report_button_enabled)

        report_abuse_box.insert_text('This is an automatically generated report.')
        Assert.true(report_abuse_box.is_report_button_enabled)

        report_abuse_box.click_report_button()

        details_page.wait_notification_box_visible()
        Assert.equal(details_page.notification_message, "Abuse reported")

    @pytest.mark.credentials
    def test_that_reports_abuse_as_signed_in_user(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)
        home_page.login(user="default")
        Assert.true(home_page.header.is_user_logged_in)

        search_page = home_page.header.search(self.search_term)

        # Select the first application link in the list
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        Assert.true(details_page.is_report_abuse_button_visible)
        report_abuse_box = details_page.click_report_abuse_button()

        Assert.true(report_abuse_box.is_visible)
        Assert.false(report_abuse_box.is_report_button_enabled)

        report_abuse_box.insert_text('This is an automatically generated report.')
        Assert.true(report_abuse_box.is_report_button_enabled)

        report_abuse_box.click_report_button()

        details_page.wait_notification_box_visible()
        Assert.equal(details_page.notification_message, "Abuse reported")
