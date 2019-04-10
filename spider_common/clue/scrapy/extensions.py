from ..api import ClueApi


class ClueApiExtension:
    """
    do ClueApi initialization
    """

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        ClueApi(api=settings.get('CLUE_API'))
