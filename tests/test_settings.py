from sense_table.settings import SenseTableSettings
from pydantic import ValidationError
from my_logging import getLogger
import unittest

logger = getLogger(__name__)


class TestSettings(unittest.TestCase):
    def test_settings(self):
        settings = SenseTableSettings()
        logger.info(settings)
        self.assertEqual(settings.heatmapNormalizeColor, 'none')

    def test_wrong_name_or_value(self):
        with self.assertRaises(ValidationError):
            SenseTableSettings(heatmapNormalizeColr='zone')

        with self.assertRaises(ValidationError):
            SenseTableSettings(heatmapNormalizeColor='unknown')

    def test_out_of_range(self):
        settings = SenseTableSettings(baseFontSize=14)
        self.assertEqual(settings.baseFontSize, 14)

        with self.assertRaises(ValidationError):
            SenseTableSettings(baseFontSize=100)

    def test_immutable(self):
        settings = SenseTableSettings()

        with self.assertRaises(ValidationError):
            settings.baseFontSize = 15


if __name__ == '__main__':
    unittest.main()


