#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import ioc
import os
import unittest2 as unittest
import yaml
from tests.ioc.service import EnvironmentVariables

current_dir = os.path.dirname(os.path.realpath(__file__))


class HelperTest(unittest.TestCase):

    def test_build(self):
        container = ioc.build([
            "%s/../fixtures/services.yml" % current_dir
        ], parameters={'inline': 'parameter'})

        self.assertEqual(6, len(container.services))
        self.assertEqual(container.get('foo').fake, container.get('fake'))
        self.assertEqual('argument 1', container.get('fake').mandatory)

        self.ok = True
        self.arg2 = True

        fake = container.get('fake')
        self.assertEqual(True, fake.ok)
        self.assertEqual("arg", fake.arg2)

        self.assertTrue(container.get('foo').weak_reference == container.get('weak_reference'))

        self.assertEqual('the argument 1', container.parameters.get('foo.foo'))
        self.assertEqual('parameter', container.parameters.get('inline'))

    def test_deepcopy(self):
        values = [
            {'sad': 1},
            ('%tuple%', 2)
        ]

        for value in values:
            self.assertEqual(value, ioc.helper.deepcopy(value))

    def test_build_container_with_parameter_env(self):
        EnvironmentVariables.set('ENVIRONMENT', 'prod')
        container = ioc.build([
            "%s/../fixtures/services.yml" % current_dir
        ], parameters={'inline': 'parameter'})

        self.assertEqual('prod', container.parameters.get('foo.env'))


class DictTest(unittest.TestCase):

    def test_dict(self):
        d = ioc.helper.Dict({'key': 'value'})

        self.assertEqual('value', d.get('key'))
        self.assertEqual(None, d.get('key.fake'))
        self.assertEqual('default', d.get('key.fake', 'default'))

        config = ioc.helper.Dict()
        managers = config.get_dict('managers', {'foo': 'bar'})

        self.assertEqual(managers.get('foo'), 'bar')

    def test_dict_iterator(self):
        d = ioc.helper.Dict({'key': 'value'})

        for key, value in d.iteritems():
            self.assertEqual(key, 'key')
            self.assertEqual(value, 'value')

    def test_all(self):
        d = ioc.helper.Dict({'key': 'value'})
        self.assertEqual(d.all(), {'key': 'value'})

        d = ioc.helper.Dict({'key': ioc.helper.Dict({'value': 'foo'})})
        self.assertEqual(d.all(), {'key': {'value': 'foo'}})

        d = ioc.helper.Dict({'key': ioc.helper.Dict({'value': ['foo', 'bar']})})
        self.assertEqual(d.all(), {'key': {'value': ['foo', 'bar']}})
