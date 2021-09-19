from open_sea_v1.endpoints.abc import ClientParams
from open_sea_v1.endpoints.events import EventsEndpoint, EventType
from open_sea_v1.responses.tests._response_helpers import ResponseTestHelper


class TestEventsObj(ResponseTestHelper):

    def setUp(self) -> None:
        self.events_kwargs = dict(
            client_params=ClientParams(limit=1, page_size=1),
            asset_contract_address="0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270",  # artblocks curated
            only_opensea=False,
        )
        self.very_rare_event_types = {EventType.BID_WITHDRAWN, EventType.APPROVE}
        self.common_event_types = [e for e in EventType.list() if e not in self.very_rare_event_types]

    def get_sample_event_response(self, event_type: EventType):
        events = self.create_and_get(EventsEndpoint, event_type=event_type, **self.events_kwargs)
        return events[0]

    def test_attributes_do_not_raise_unexpected_exceptions(self):
        for event_type in self.common_event_types:
            event = self.get_sample_event_response(event_type)  # type: ignore
            self.assert_attributes_do_not_raise_unexpected_exceptions(event)

    def test_no_missing_class_attributes_from_original_json_keys(self):
        for event_type in self.common_event_types:
            event = self.get_sample_event_response(event_type)  # type: ignore
            self.assert_no_missing_class_attributes_from_original_json_keys(response_obj=event, json=event._json)
