from pynwb.form.build import GroupBuilder, DatasetBuilder

from pynwb.core import DynamicTable

from . import base

import pandas as pd


class TestDynamicTableIO(base.TestMapRoundTrip):

    def setUpContainer(self):
        return DynamicTable('trials', 'DynamicTable integration test', 'a test table')

    def setUpBuilder(self):
        id_builder = DatasetBuilder('id', data=[],
                                    attributes={
                                         'help': 'unique identifiers for a list of elements',
                                         'namespace': 'core',
                                         'neurodata_type': 'ElementIdentifiers',
                                    })
        return GroupBuilder('trials',
                            attributes={
                                'help': 'A column-centric table',
                                'description': 'a test table',
                                'namespace': 'core',
                                'neurodata_type': 'DynamicTable',
                                'source': 'DynamicTable integration test',
                                'colnames': tuple(),

                            },
                            datasets={'id': id_builder})

    def addContainer(self, nwbfile):
        nwbfile.trials = self.container

    def getContainer(self, nwbfile):
        return nwbfile.trials


class TestTrials(base.TestMapRoundTrip):

    def setUpContainer(self):
        # this will get ignored
        return DynamicTable('trials', 'DynamicTable integration test', 'a placeholder table')

    def addContainer(self, nwbfile):
        nwbfile.add_trial_column('foo', 'an int column')
        nwbfile.add_trial_column('bar', 'a float column')
        nwbfile.add_trial_column('baz', 'a string column')
        nwbfile.add_trial_column('qux', 'a boolean column')
        nwbfile.add_trial({'start': 0., 'end': 1., 'foo': 27, 'bar': 28.0, 'baz': "29", 'qux': True})
        nwbfile.add_trial({'start': 2., 'end': 3., 'foo': 37, 'bar': 38.0, 'baz': "39", 'qux': False})
        # reset the thing
        self.container = nwbfile.trials

    def getContainer(self, nwbfile):
        return nwbfile.trials


class TestUnits(base.TestMapRoundTrip):

    def setUpContainer(self):
        # this will get ignored
        return DynamicTable('units', 'unit table integration test', 'a placeholder table')

    def addContainer(self, nwbfile):
        nwbfile.add_unit_column('foo', 'an int column')
        nwbfile.add_unit({'foo': 27})
        nwbfile.add_unit({'foo': 37})
        # reset the thing
        self.container = nwbfile.units

    def getContainer(self, nwbfile):
        return nwbfile.units


class TestUnitsDf(base.TestMapRoundTrip):

    def setUpContainer(self):
        # this will get ignored
        return DynamicTable('units', 'unit table integration test', 'a placeholder table')

    def addContainer(self, nwbfile):
        nwbfile.units = DynamicTable.from_dataframe(pd.DataFrame({
            'a': [1, 2, 3],
            'b': ['4', '5', '6']
        }), 'units', 'a_source')
        # reset the thing
        self.container = nwbfile.units

    def getContainer(self, nwbfile):
        return nwbfile.units


class TestElectrodes(base.TestMapRoundTrip):

    def setUpContainer(self):
        return DynamicTable('electrodes', 'metadata about extracellular electrodes', 'autogenerated by PyNWB API')

    def addContainer(self, nwbfile):
        ''' Should take an NWBFile object and add the container to it '''
        self.dev1 = nwbfile.create_device('dev1', 'a test source')  # noqa: F405
        self.group = nwbfile.create_electrode_group('tetrode1', 'a test source',  # noqa: F405
                                    'tetrode description', 'tetrode location', self.dev1)

        nwbfile.add_electrode(id=1, x=1.0, y=2.0, z=3.0, imp=-1.0, location='CA1', filtering='none', group=self.group,
                              group_name='tetrode1')
        nwbfile.add_electrode(id=2, x=1.0, y=2.0, z=3.0, imp=-2.0, location='CA1', filtering='none', group=self.group,
                              group_name='tetrode1')
        nwbfile.add_electrode(id=3, x=1.0, y=2.0, z=3.0, imp=-3.0, location='CA1', filtering='none', group=self.group,
                              group_name='tetrode1')
        nwbfile.add_electrode(id=4, x=1.0, y=2.0, z=3.0, imp=-4.0, location='CA1', filtering='none', group=self.group,
                              group_name='tetrode1')
        self.container = nwbfile.electrodes

    def getContainer(self, nwbfile):
        return nwbfile.electrodes

    def test_roundtrip(self):
        super(TestElectrodes, self).test_roundtrip()
        self.assertContainerEqual(self.read_container[0][7], self.container[0][7])
