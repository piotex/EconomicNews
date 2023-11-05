from dataclasses import dataclass


@dataclass
class model_news:
    url: str = ""
    header: str = ""
    quick_info: str = ""
    creation_time: str = ""
    parser_header: str = ""
    parser_quick_info: str = ""
    comments_number: int = -1

    # unit_price: float
    # quantity_on_hand: int = 0
    #
    # def total_cost(self) -> float:
    #     return self.unit_price * self.quantity_on_hand
