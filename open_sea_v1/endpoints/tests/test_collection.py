# from unittest import TestCase
#
# from open_sea_v1.endpoints.endpoint_base_client import OpenSeaClient
#
#
# class TestCollectionsRequests(TestCase):
#     client = CLIENT
#     collections_limit = 7
#     collections_offset = 0
#     collections = client.collections(offset=collections_offset, limit=collections_limit)
#     collection = collections[0]  # default resp
#
#     def test_collections_request_returns_valid_response(self):
#         self.assertTrue(self.collection)
#
#     def test_collections_request_limit_param(self):
#         self.assertEqual(len(self.collections), self.collections_limit)
#
#     def test_collections_request_offset_param(self):
#         raise NotImplementedError()
#         offset_collections = self.client.collections(limit=self.collections_limit, offset=self.collections_offset + 1)
#         self.assertNotEqual(self.collections[0]['name'], offset_collections[0]['name'])
#         self.assertNotEqual(self.collections[-1]['name'], offset_collections[-1]['name'])
#         self.assertEqual(self.collections[-2]['name'], offset_collections[-1]['name'])
#         self.assertEqual(self.collections[-2]['name'], offset_collections[-1]['name'])
#
#     def test_collections_api_key_http_header_was_passed(self):
#         api_client = OpenSeaClient(api_key='randomstuff')
#         resp = api_client._collections(limit=1, offset=0)
#         self.assertIn('X-API-Key', dict(resp.request.headers))