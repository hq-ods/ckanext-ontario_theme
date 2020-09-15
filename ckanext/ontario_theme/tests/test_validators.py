# encoding: utf-8

'''Unit tests for ontario_theme/tests/test_validators.py
'''
import nose.tools
import ckanext.ontario_theme.plugin as ontario_theme

assert_equals = nose.tools.assert_equals

import ckan.model as model
import ckan.plugins
import ckan.tests.factories as factories

import ckan.tests.helpers as helpers

class TestOntarioThemeCopyFluentKeywordsToTags(object):
    '''Ensure Fluent multi-lingual keywords are copied to CKAN core Tags.
    '''

    @classmethod
    def setup_class(cls):
        '''Nose runs this method once to setup our test class.'''
        # Test code should use CKAN's plugins.load() function to load plugins
        # to be tested.
        ckan.plugins.load('ontario_theme')

    def teardown(self):
        '''Nose runs this method after each test method in our test class.'''
        # Rebuild CKAN's database after each test method, so that each test
        # method runs with a clean slate.
        model.repo.rebuild_db()

    @classmethod
    def teardown_class(cls):
        '''Nose runs this method once after all the test methods in our class
        have been run.

        '''
        # We have to unload the plugin we loaded, so it doesn't affect any
        # tests that run after ours.
        ckan.plugins.unload('ontario_theme')

    def test_ontario_theme_copy_fluent_keywords_to_tags(self):
        '''If a dataset's keywords are updated make sure the Tags are too.
        These copied keywords should be available from the tag_autocomplete
        action.
        '''

        assert_equals(helpers.call_action('tag_autocomplete',
            query='Engl'), [])

        org = factories.Organization()
        dataset = helpers.call_action(
            'package_create',
            name = 'package-name',
            maintainer_translated = {
                'en': u'Joe Smith',
                'fr': u'...'
            },
            maintainer_email = 'Joe.Smith@ontario.ca',
            title_translated = {
                'en': u'A Novel By Tolstoy',
                'fr':u'Un novel par Tolstoy'
            },
            notes_translated = {
                'en': u'short description',
                'fr': u'...'
            },
            owner_org = org['name'], # depends on config.
            keywords = {
                'en': [u'English', u'Language'],
                'fr': [u'Français'],
                'de': [u'...']
            },
        )

        assert_equals(dataset['keywords'], {
                'en': [u'English', u'Language'],
                'fr': [u'Français'],
                'de': [u'...']
            })
        assert_equals(
            sorted([tag['name'] for tag in dataset['tags']]),
            [u'...', u'English', u'Français', u'Language']
        )

        assert_equals(helpers.call_action('tag_autocomplete',
            query='Engl'), [u'English'])
