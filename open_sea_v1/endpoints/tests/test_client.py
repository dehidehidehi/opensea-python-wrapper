from itertools import chain
from os import environ
from unittest import TestCase, skipIf

from open_sea_v1.endpoints.client import ClientParams
from open_sea_v1.endpoints.events import EventsEndpoint, EventType
from open_sea_v1.responses.event import EventResponse
from open_sea_v1.tests.run_tests import SKIP_SLOW_TESTS


class TestClientParams(TestCase):

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
            client_params=ClientParams(max_pages=cls.max_pages, limit=cls.limit, page_size=cls.limit),  # type: ignore
            asset_contract_address="0x76be3b62873462d2142405439777e971754e8e77",
            token_id=str(10152),
            event_type=EventType.SUCCESSFUL,
        )
        cls.sample_pages = cls.mk_events_endpoint().get_parsed_pages(flat=False)

    def setUp(self) -> None:
        self.sample_client = self.mk_events_endpoint()

    @classmethod
    def mk_events_endpoint(cls) -> EventsEndpoint:
        return EventsEndpoint(**cls.sample_client_kwargs)  # type: ignore

    def test_remaining_pages_true_if_json_resp_is_none(self):
        self.sample_client._latest_json_response = None
        self.assertTrue(self.sample_client._remaining_pages())

    def test_get_pages_does_not_append_empty_pages(self):
        no_empty_pages = all(not page == list() for page in self.sample_pages)
        self.assertTrue(no_empty_pages)

    def test_get_pages_max_pages_and_limit_params_works(self):
        self.assertLessEqual(len(self.sample_pages), self.max_pages)
        for page in self.sample_pages[:-1]:
            self.assertEqual(self.limit, len(page))

    def test_pagination_does_not_return_duplicates_between_different_pages(self):
        limit = 2
        max_pages = 2
        self.sample_client.client_params = ClientParams(limit=limit, page_size=limit, max_pages=max_pages)
        events_resps: list[EventResponse] = self.sample_client.get_parsed_pages()
        unique_ids = set(e.id for e in events_resps)
        self.assertEqual(len(unique_ids), limit * max_pages)

    def test_pagination_pages_are_in_perfect_sequence(self):
        """Making sure we are not skipping things between pages by mistake."""
        self.sample_client.client_params = ClientParams(limit=1, offset=0, page_size=1, max_pages=2)
        resp_1_ids = [e.id for e in self.sample_client.get_parsed_pages()]
        self.sample_client.client_params = ClientParams(limit=1, offset=1, page_size=1, max_pages=1)
        resp_2_ids = [e.id for e in self.sample_client.get_parsed_pages()]
        # print(resp_1_ids)
        # print(resp_2_ids)
        self.assertEqual(resp_1_ids[-1], resp_2_ids[-1])


@skipIf(not environ.get('OPENSEA_API_KEY'), "No OPENSEA_API_KEY detected within system environment variables.")
class TestBaseClientAsyncWithAPIKey(TestCase):

    def setUp(self) -> None:
        client_params = ClientParams(max_pages=1)
        self.sample_client = EventsEndpoint(
            client_params=client_params,
            asset_contract_address="0x76be3b62873462d2142405439777e971754e8e77",
            event_type=EventType.SUCCESSFUL,
        )

    def test_api_key_is_automatically_registered_in_client_params_from_system_environment_variables(self):
        client_params_has_api_key = bool(self.sample_client.client_params.api_key)
        self.assertTrue(client_params_has_api_key)

    def test_async_client_works_with_only_one_page_requested(self):
        self.sample_client.client_params.max_pages = 1
        pages = self.sample_client.get_parsed_pages()
        self.assertGreaterEqual(len(pages), 1)

    def test_async_client_returns_expected_number_of_pages(self):
        self.sample_client.client_params.max_pages = 3
        consumed_responses = self.sample_client.get_parsed_pages()
        self.assertGreaterEqual(len(consumed_responses), 3)

    @skipIf(SKIP_SLOW_TESTS, "Skipping long API query.")
    def test_request_not_throttled_if_client_param_max_pages_attr_is_set_to_high(self):
        self.sample_client.client_params = ClientParams(max_pages=10)
        self.sample_client.get_parsed_pages()

    @skipIf(SKIP_SLOW_TESTS, "Skipping long API query.")
    def test_request_not_throttled_if_client_param_max_pages_attr_is_set_to_infinite(self):
        self.sample_client.client_params = ClientParams(max_pages=None)
        self.sample_client.get_parsed_pages()

    def test_get_parsed_pages_flat_true_returns_flattened_list(self):
        self.sample_client.client_params = ClientParams(max_pages=3, page_size=2, limit=2)
        results = self.sample_client.get_parsed_pages()
        self.assertEqual(6, len(results))

    def test_async_batch_request_does_not_return_duplicate_event_ids(self):
        parsed = self.sample_client.get_parsed_pages()
        event_ids = [n.id for n in parsed]
        unique_event_ids = set(event_ids)
        self.assertEqual(len(event_ids), len(unique_event_ids))
