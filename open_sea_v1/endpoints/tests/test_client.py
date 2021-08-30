from itertools import chain
from unittest import TestCase

from open_sea_v1.endpoints.client import ClientParams
from open_sea_v1.endpoints.events import EventsEndpoint, EventType


class TestClientParams(TestCase):

    def test_max_pages_attr_is_automatically_decremented_by_1(self):
        params = ClientParams(max_pages=1)
        self.assertEqual(params.max_pages, 0)

    def test_max_pages_attr_raises_value_error_if_below_or_equal_to_zero(self):
        self.assertRaises(ValueError, ClientParams, max_pages=-1)

    def test_limit_attr_raises_value_error_if_not_between_0_and_300(self):
        self.assertRaises(ValueError, ClientParams, limit=-1)
        self.assertRaises(ValueError, ClientParams, limit=301)

    def test_page_size_attr_raises_value_error_if_not_between_0_and_50(self):
        self.assertRaises(ValueError, ClientParams, page_size=-1)
        self.assertRaises(ValueError, ClientParams, page_size=51)


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
        cls.sample_pages = list(cls.mk_events_endpoint().get_pages())

    def setUp(self) -> None:
        self.sample_client = self.mk_events_endpoint()

    @classmethod
    def mk_events_endpoint(cls) -> EventsEndpoint:
        return EventsEndpoint(**cls.sample_client_kwargs)

    def test_remaining_pages_true_if_http_response_is_none(self):
        self.sample_client._http_response = None
        self.assertTrue(self.sample_client.remaining_pages())

    def test_remaining_pages_does_not_raise_if_client_params_all_none(self):
        updated_kwargs = self.sample_client_kwargs | dict(client_params=ClientParams(max_pages=None, api_key=None))
        client = EventsEndpoint(**updated_kwargs)
        next(client.get_pages())
        client.remaining_pages()  # assert not raises

    def test_get_pages_does_not_append_empty_pages(self):
        no_empty_pages = all(not page == list() for page in self.sample_pages)
        self.assertTrue(no_empty_pages)

    def test_get_pages_max_pages_and_limit_params_works(self):
        self.assertLessEqual(len(self.sample_pages), self.max_pages + 1)
        for page in self.sample_pages[:-1]:
            self.assertEqual(self.limit, len(page))

    def test_pagination_does_not_return_duplicates_between_different_pages(self):

        def get_event_ids(offset) -> list[str]:
            self.sample_client.client_params = ClientParams(limit=5, offset=offset, max_pages=1)
            return [event.id for event in chain.from_iterable(self.sample_client.get_pages())]

        pages = [get_event_ids(offset) for offset in range(0, 14, 5)]
        pages = list(chain.from_iterable(pages))
        total_events = len(pages)
        total_unique_events = len(set(pages))
        self.assertEqual(total_events, total_unique_events)

    def test_pagination_pages_are_in_perfect_sequence(self):
        """Making sure we are not skipping things between pages by mistake."""
        self.sample_client.client_params = ClientParams(limit=2, offset=0, max_pages=1)
        short_page_event_ids = [e.id for e in list(self.sample_client.get_pages())[0]]
        self.sample_client.client_params = ClientParams(limit=3, offset=1, max_pages=1)
        longer_page_event_ids = [e.id for e in list(self.sample_client.get_pages())[0]]
        self.assertEqual(short_page_event_ids[-1], longer_page_event_ids[0])
