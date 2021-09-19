from open_sea_v1.endpoints.abc import ClientParams
from open_sea_v1.endpoints.events import EventsEndpoint, EventType
from open_sea_v1.responses.tests._response_helpers import ResponseTestHelper


class TestEventsObj(ResponseTestHelper):

    def setUp(self) -> None:
        self.events_kwargs = dict(
            client_params=ClientParams(limit=1, page_size=1, max_pages=1),
            asset_contract_address="0xa08126f5e1ed91a635987071e6ff5eb2aeb67c48",
        )
        self.common_events = [EventType.CREATED, EventType.SUCCESSFUL]
        # Other event types are too rare, and almost don't happen even on the most popular collections.

    def get_sample_event_response(self, event_type: EventType):
        events = self.create_and_get(EventsEndpoint, event_type=event_type, **self.events_kwargs)
        try:
            return events.pop()
        except IndexError as err:
            raise IndexError(f"{event_type}, {err}")

    def test_attributes_do_not_raise_unexpected_exceptions(self):
        for event_type in self.common_events:
            event = self.get_sample_event_response(event_type)  # type: ignore
            self.assert_attributes_do_not_raise_unexpected_exceptions(event)

    def test_no_missing_class_attributes_from_original_json_keys(self):
        for event_type in self.common_events:
            event = self.get_sample_event_response(event_type)  # type: ignore
            self.assert_no_missing_class_attributes_from_original_json_keys(response_obj=event, json=event._json)
