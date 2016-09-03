"""
Tests for who-data ingest module's library functions and classes
"""

from who_data.bin.ingest.tests import TestBase


class file_hash(TestBase):

    def test(self):
        from who_data.bin.ingest.lib.file_hash import file_hash
        test_hash = file_hash(
            'who_data/bin/ingest/tests/test_file_for_md5.txt'
        )
        self.assertEquals(
            test_hash,
            '22913813f7586afbc34b168468027a2d'
        )
