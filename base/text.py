from base.saves import properties

class TextTranslationLoader:
    instance = None

    def __init__(self, langfile):
        TextTranslationLoader.instance = self
        self.language = properties.PropertiesLoader.load_file(langfile)


def text_translation(key):
    return TextTranslationLoader.instance.language[key]
