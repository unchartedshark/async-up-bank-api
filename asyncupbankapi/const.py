from enum import Enum

BASE_URL = "https://api.up.com.au/api/v1"
PAGE_SIZE = "page[size]"


class AccountType(Enum):
    SAVER = "SAVER"
    TRANSACTIONAL = "TRANSACTIONAL"


class TransactionStatus(Enum):
    HELD = "HELD"
    SETTLED = "SETTLED"


class WebhookEventType(Enum):
    CREATED = "TRANSACTION_CREATED"
    SETTLED = "TRANSACTION_SETTLED"
    DELETED = "TRANSACTION_DELETED"
    PING = "PING"


class WebhookDeliveryStatus(Enum):
    DELIVERED = "DELIVERED"
    UNDELIVERABLE = "UNDELIVERABLE"
    BAD_RESPONSE_CODE = "BAD_RESPONSE_CODE"
