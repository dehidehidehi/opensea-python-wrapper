from open_sea_v1.endpoints import EventsEndpoint, EventType
from open_sea_v1.responses.tests._response_helpers import ResponseTestHelper


class TestEventsObj(ResponseTestHelper):
    sample_contract = "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb"  # punk
    events_default_kwargs = dict(
        offset=0, limit=1, asset_contract_address=sample_contract,
        only_opensea=False, event_type=EventType.SUCCESSFUL,
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.events = cls.create_and_get(EventsEndpoint, **cls.events_default_kwargs)
        cls.event = cls.events[0]

    def test_attributes_do_not_raise_unexpected_exceptions(self):
        self.assert_attributes_do_not_raise_unexpected_exceptions(self.event)

    def test_no_missing_class_attributes_from_original_json_keys(self):
        self.assert_no_missing_class_attributes_from_original_json_keys(response_obj=self.event, json=self.event._json)
