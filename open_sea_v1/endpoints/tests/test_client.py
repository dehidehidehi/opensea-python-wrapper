from itertools import chain
from unittest import TestCase

from open_sea_v1.endpoints.client import ClientParams
from open_sea_v1.endpoints.events import EventsEndpoint, EventType


class TestBaseEndpointClient(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.max_pages = 2
        cls.limit = 5
        cls.sample_client_kwargs = dict(
            client_params=ClientParams(max_pages=cls.max_pages, limit=cls.limit),
            asset_contract_address="0x76be3b62873462d2142405439777e971754e8e77",
            token_id=str(10152),
            event_type=EventType.SUCCESSFUL,
        )
        cls.sample_client = EventsEndpoint(**cls.sample_client_kwargs)
        cls.sample_pages = list(cls.sample_client.get_pages())

    def test_remaining_pages_true_if_http_response_is_none(self):
        self.sample_client._http_response = None
        self.assertTrue(self.sample_client.remaining_pages())

    def test_remaining_pages_does_not_raise_if_client_params_all_none(self):
        updated_kwargs = self.sample_client_kwargs | dict(client_params=ClientParams(max_pages=None, api_key=None))
        client = EventsEndpoint(**updated_kwargs)
        next(client.get_pages())
        client.remaining_pages()  # assert not raises

    def test_get_pages_resets_processed_pages_and_offset_attr_on_new_calls(self):
        for _ in range(2):
            next(self.sample_client.get_pages())
            self.assertEqual(self.sample_client.processed_pages, 1)
            expected_offset_value = self.sample_client.client_params.limit
            self.assertEqual(self.sample_client.client_params.offset, expected_offset_value)

    def test_get_pages_does_not_append_empty_pages(self):
        no_empty_pages = all(not page == list() for page in self.sample_pages)
        self.assertTrue(no_empty_pages)

    def test_get_pages_max_pages_and_limit_params_works(self):
        self.assertLessEqual(len(self.sample_pages), self.max_pages + 1)
        for page in self.sample_pages[:-1]:
            self.assertEqual(self.limit, len(page))

    def test_pagination_works(self):
        id_list_1 = [[e.id for e in page] for page in self.sample_client.get_pages()]
        id_list_1 = list(chain.from_iterable(id_list_1))
        id_list_1.sort(reverse=True)

        self.sample_client.client_params = ClientParams(limit=4, offset=0, max_pages=2)
        id_list_2 = [[e.id for e in page] for page in self.sample_client.get_pages()]
        id_list_2 = list(chain.from_iterable(id_list_2))
        id_list_2.sort(reverse=True)

        self.assertEqual(len(id_list_2), 12)  # updated limit * max_pages+1
        self.assertGreater(len(id_list_1), len(id_list_2))
        self.assertTrue(id_list_1[i] == id_list_2[i] for i in range(len(id_list_2)))

    def test_pagination_does_not_return_duplicates_between_different_pages(self):
        raise NotImplementedError
        self.sample_client.client_params = ClientParams(limit=5, offset=0, max_pages=1)
        page_1_event_ids = [e.event_id for e in self.sample_client.get_pages()]
        self.sample_client.client_params = ClientParams(limit=5, offset=5, max_pages=1)
        page_2_event_ids = self.sample_client.get_pages()
        self.sample_client.client_params = ClientParams(limit=5, offset=10, max_pages=1)
        page_3_event_ids = self.sample_client.get_pages()
        ...
