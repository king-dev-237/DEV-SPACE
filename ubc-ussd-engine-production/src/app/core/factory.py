# app/core/factory.py
class USSDFeatureFactory:
    def __init__(self):
        self._features = {}

    def register_feature(self, name, feature_class):
        self._features[name] = feature_class

    def get_feature(self, name):
        feature = self._features.get(name)
        if not feature:
            raise ValueError(f"Feature {name} not found")
        return feature()


class AccountDetailsFactory:
    def __init__(self):
        self.account_number = None
        self.account_rib = None
        self.account_agency = None
        self.account_balance_SDE = None
        self.account_balance_SDI = None
        self.account_balance_SDC = None
        self.account_chapitre = None
        self.account_type = None


class ClientDetailsFactory:
    def __init__(self):
        self.account_details = {}
        self.client_id = None
        self.client_name = None
        self.client_type = None
        self.client_phone_number = None
        self.client_email = None


class USSDSubscriberFactory:
    def __init__(self):
        self.subscriber_phone_number = None
        self.subscriber_id = None
        self.subscriber_type = None
        self.subscriber_name = None

