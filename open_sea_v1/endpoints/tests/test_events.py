from datetime import datetime, timedelta
from unittest import TestCase

from open_sea_v1.endpoints.client import ClientParams
from open_sea_v1.endpoints.events import EventsEndpoint, EventType, AuctionType


class TestEventsEndpoint(TestCase):
    events_default_kwargs = dict(
        client_params=ClientParams(limit=1, page_size=1),
        asset_contract_address="0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb",  # punk
        event_type=EventType.SUCCESSFUL,
    )

    @staticmethod
    def create_and_get(**kwargs):
        endpoint = EventsEndpoint(**kwargs)
        endpoint._get_request()
        return endpoint.parsed_http_response

    def test_param_event_type_filters_properly(self):
        updated_kwargs = self.events_default_kwargs | dict(client_params=ClientParams(limit=5, page_size=5))
        punks_events = self.create_and_get(**updated_kwargs)
        self.assertTrue(all(e.event_type == EventType.SUCCESSFUL for e in punks_events))

    def test_param_event_type_raises_if_not_from_event_type_enum_values(self):
        updated_kwargs = self.events_default_kwargs | dict(event_type='randomstr')
        self.assertRaises((ValueError, TypeError), self.create_and_get, **updated_kwargs)

    def test_param_auction_type_filters_properly(self):
        new_client_params = ClientParams(limit=5, page_size=5)
        updated_kwargs = self.events_default_kwargs | dict(client_params=new_client_params, auction_type=AuctionType.DUTCH)
        punks_events = self.create_and_get(**updated_kwargs)
        self.assertTrue(all(e.auction_type == AuctionType.DUTCH for e in punks_events))

    def test_param_auction_type_raises_if_not_from_auction_type_enum_values(self):
        updated_kwargs = self.events_default_kwargs | dict(auction_type='randomstr')
        self.assertRaises((ValueError, TypeError), self.create_and_get, **updated_kwargs)

    def test_param_auction_type_raises_if_not_isinstance_of_str(self):
        updated_kwargs = self.events_default_kwargs | dict(auction_type=0.0)  # type: ignore
        self.assertRaises((ValueError, TypeError), self.create_and_get, **updated_kwargs)

    def test_param_auction_type_does_not_raise_if_is_none(self):
        updated_kwargs = self.events_default_kwargs | dict(auction_type=None)  # type: ignore
        self.create_and_get(**updated_kwargs)

    def test_param_only_opensea_true_filters_properly(self):
        new_client_params = ClientParams(limit=2, page_size=2)
        updated_kwargs = self.events_default_kwargs | dict(only_opensea=True, client_params=new_client_params)
        events = self.create_and_get(**updated_kwargs)
        self.assertTrue(all('opensea.io' in event.asset.permalink for event in events))

    def test_param_only_opensea_false_does_not_filter(self):
        """
        Have no idea how to test this param.
        """
        # updated_kwargs = self.events_kwargs | dict(only_opensea=False, offset=1, limit=100)
        # events = self.create_and_get(**updated_kwargs)
        # self.assertTrue(any('opensea.io' not in event.asset.permalink for event in events))
        pass

    def test_param_occurred_before_raises_exception_if_not_datetime_instances(self):
        updated_kwargs = self.events_default_kwargs | dict(occurred_before=True)  # type: ignore
        self.assertRaises(TypeError, self.create_and_get, **updated_kwargs)

    def test_param_occurred_before_and_after_raises_exception_if_are_equal_values(self):
        dt_now = datetime.now()
        occurred_params = dict(occurred_before=dt_now, occurred_after=dt_now)
        updated_kwargs = self.events_default_kwargs | occurred_params  # type: ignore
        self.assertRaises(ValueError, self.create_and_get, **updated_kwargs)

    def test_param_occurred_before_and_after_does_not_raise_if_both_are_none(self):
        updated_kwargs = self.events_default_kwargs | dict(occurred_before=None, occurred_after=None)  # type: ignore
        self.create_and_get(**updated_kwargs)

    def test_param_occurred_after_cannot_be_higher_than_occurred_before(self):
        occurred_before = datetime.now()
        occurred_after = occurred_before + timedelta(microseconds=1)
        occurred_params = dict(occurred_before=occurred_before, occurred_after=occurred_after)
        updated_kwargs = self.events_default_kwargs | occurred_params  # type: ignore
        self.assertRaises(ValueError, self.create_and_get, **updated_kwargs)

    def test_param_occurred_after_filters_properly(self):
        occurred_after = datetime(year=2021, month=8, day=1)
        new_client_params = ClientParams(limit=5, page_size=5)
        updated_kwargs = self.events_default_kwargs | dict(occurred_after=occurred_after, client_params=new_client_params)
        events = self.create_and_get(**updated_kwargs)
        transaction_datetimes = [datetime.fromisoformat(event.transaction['timestamp']) for event in events]
        self.assertTrue(all(trans_date >= occurred_after for trans_date in transaction_datetimes))

    def test_param_occurred_before_filters_properly(self):
        occurred_before = datetime(year=2021, month=8, day=1)
        new_client_params = ClientParams(limit=5, page_size=5)
        updated_kwargs = self.events_default_kwargs | dict(occurred_before=occurred_before, client_params=new_client_params)
        events = self.create_and_get(**updated_kwargs)
        transaction_datetimes = [datetime.fromisoformat(event.transaction['timestamp']) for event in events]
        self.assertTrue(all(trans_date < occurred_before for trans_date in transaction_datetimes))

    def test_params_occurred_before_after_work_together(self):
        occurred_after = datetime(year=2021, month=7, day=30)
        occurred_before = datetime(year=2021, month=8, day=2)
        new_client_params = ClientParams(limit=5, page_size=5)
        kwargs = dict(occurred_after=occurred_after, occurred_before=occurred_before, client_params=new_client_params)
        updated_kwargs = self.events_default_kwargs | kwargs
        events = self.create_and_get(**updated_kwargs)
        transaction_datetimes = [datetime.fromisoformat(event.transaction['timestamp']) for event in events]
        self.assertTrue(all(occurred_after <= trans_date <= occurred_before for trans_date in transaction_datetimes))