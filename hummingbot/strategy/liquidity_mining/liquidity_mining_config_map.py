from decimal import Decimal
from typing import Optional
from hummingbot.client.config.config_var import ConfigVar
from hummingbot.client.config.config_validators import (
    validate_exchange,
    validate_decimal,
    validate_int
)
from hummingbot.client.settings import (
    required_exchanges,
)


def exchange_on_validated(value: str) -> None:
    required_exchanges.append(value)


def token_validate(value: str) -> Optional[str]:
    value = value.upper()
    markets = list(liquidity_mining_config_map["markets"].value.split(","))
    tokens = set()
    for market in markets:
        tokens.update(set(market.split("-")))
    if value not in tokens:
        return f"Invalid token. {value} is not one of {','.join(tokens)}"


def order_size_prompt() -> str:
    token = liquidity_mining_config_map["token"].value
    return f"What is the size of each order (in {token} amount)? >>> "


liquidity_mining_config_map = {
    "strategy": ConfigVar(
        key="strategy",
        prompt="",
        default="liquidity_mining"),
    "exchange":
        ConfigVar(key="exchange",
                  prompt="Enter your liquidity mining exchange name >>> ",
                  validator=validate_exchange,
                  on_validated=exchange_on_validated,
                  prompt_on_new=True),
    "markets":
        ConfigVar(key="markets",
                  prompt="Enter a list of markets (comma separated, e.g. LTC-USDT,ETH-USDT) >>> ",
                  type_str="str",
                  prompt_on_new=True),
    "spread":
        ConfigVar(key="spread",
                  prompt="How far away from the mid price do you want to place bid and ask orders? "
                         "(Enter 1 to indicate 1%) >>> ",
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, 0, 100, inclusive=False),
                  prompt_on_new=True),
    "reserved_balances":
        ConfigVar(key="reserved_balances",
                  prompt="Enter a list of tokens and their reserved balance (to not be used by the bot), "
                         " e.g. BTC:0.1,BNB:1 >>> ",
                  type_str="str",
                  default="",
                  validator=lambda s: None,
                  prompt_on_new=True),
    "market_budget_usd":
        ConfigVar(key="market_budget_usd",
                  prompt="What is budget, in USD amount, for each market?  >>> ",
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, 0, inclusive=False),
                  prompt_on_new=True),
    "order_refresh_time":
        ConfigVar(key="order_refresh_time",
                  prompt="How often do you want to cancel and replace bids and asks "
                         "(in seconds)? >>> ",
                  type_str="float",
                  validator=lambda v: validate_decimal(v, 0, inclusive=False),
                  default=10.),
    "order_refresh_tolerance_pct":
        ConfigVar(key="order_refresh_tolerance_pct",
                  prompt="Enter the percent change in price needed to refresh orders at each cycle "
                         "(Enter 1 to indicate 1%) >>> ",
                  type_str="decimal",
                  default=Decimal("0.2"),
                  validator=lambda v: validate_decimal(v, -10, 10, inclusive=True)),
    "inventory_range_multiplier":
        ConfigVar(key="inventory_range_multiplier",
                  prompt="What is your tolerable range of inventory around the target, "
                         "expressed in multiples of your total order size? ",
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, min_value=0, inclusive=False),
                  default=Decimal("1")),
    "volatility_interval":
        ConfigVar(key="volatility_interval",
                  prompt="What is an interval, in second, in which to pick historical mid price data from to calculate "
                         "market volatility? >>> ",
                  type_str="int",
                  validator=lambda v: validate_int(v, min_value=1, inclusive=False),
                  default=60 * 5),
    "avg_volatility_period":
        ConfigVar(key="avg_volatility_period",
                  prompt="How many interval does it take to calculate average market volatility? >>> ",
                  type_str="int",
                  validator=lambda v: validate_int(v, min_value=1, inclusive=False),
                  default=10),
    "volatility_to_spread_multiplier":
        ConfigVar(key="volatility_to_spread_multiplier",
                  prompt="Enter a multiplier used to convert average volatility to spread "
                         "(enter 1 for 1 to 1 conversion) >>> ",
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, min_value=0, inclusive=False),
                  default=Decimal("1")),
}