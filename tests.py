import unittest

from instance_fetcher import get_regions, get_instances


class TestStringMethods(unittest.TestCase):

    def test_get_regions_with_default_correct_credentials(self):
        regions = get_regions()
        self.assertTrue(len(regions) > 0)

    def test_get_regions_with_incorrect_aws_access_key(self):
        regions = get_regions(aws_access_key_id="AKIA5OTURWZJO5J4PSPB_AND_MORE")
        self.assertTrue(len(regions) == 0)

    def test_get_regions_with_incorrect_aws_secret_key(self):
        regions = get_regions(aws_secret_access_key="FoZaYFiq7rJWaSUne/6qck7ntvM6CRRD6j3Ls03T_MOREEE")
        self.assertTrue(len(regions) == 0)

    def test_get_instances_with_default_correct_credentials(self):
        regions = get_regions()
        instances = get_instances(regions=regions)
        self.assertTrue(len(instances) > 0)

    def test_get_instances_with_incorrect_aws_access_key(self):
        regions = get_regions()
        instances = get_instances(regions=regions, aws_access_key_id="AKIA5OTURWZJO5J4PSPB_AND_MORE")
        self.assertTrue(len(instances) == 0)

    def test_get_instances_with_incorrect_aws_secret_key(self):
        regions = get_regions()
        instances = get_instances(regions=regions, aws_secret_access_key="FoZaYFiq7rJWaSUne/6qck7ntvM6CRRD6j3Ls03T_MOREEE")
        self.assertTrue(len(instances) == 0)

    def test_get_instances_with_none_regions_set(self):
        instances = get_instances()
        self.assertTrue(len(instances) == 0)

    def test_get_instances_with_empty_regions_set(self):
        instances = get_instances(regions=[])
        self.assertTrue(len(instances) == 0)


if __name__ == '__main__':
    unittest.main()
