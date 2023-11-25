from dataclasses import dataclass


@dataclass
class NewsModel:
    id: int = -1
    url: str = ""
    header: str = ""
    quick_info: str = ""
    creation_time: str = ""
    comments_number: int = -1
    screen_path: str = ""
    audio_quick_info_mp3_path: str = ""
    audio_quick_info_vvt_path: str = ""
    video_quick_info_gif_path: str = ""
    video_quick_info_mp4_path: str = ""


    audio_quick_info_path: str = ""
    audio_header_path: str = ""

    # unit_price: float
    # quantity_on_hand: int = 0
    #
    # def total_cost(self) -> float:
    #     return self.unit_price * self.quantity_on_hand
