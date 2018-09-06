import logging
from babel.messages import catalog, extract, mofile, pofile
from pathlib import Path

from app import config

SUPPORTED_LANGUAGES = ['ru', 'en']


class TranslationsUpdater:
    def __init__(self,
                 locale_dir: Path = config.APP_DIR.joinpath('i18n'),
                 sources_dir: Path = config.APP_DIR):
        self.locale_dir = locale_dir
        self.sources_dir = sources_dir

    def is_translations_generated(self) -> bool:
        for lang in SUPPORTED_LANGUAGES:
            if not self.locale_dir.joinpath(lang, 'LC_MESSAGES', 'zordon.mo').is_file():
                return False
        return True

    def regenerate_translations(self) -> bool:
        new_catalog = self._build_strings_catalog_from_sources()
        is_complete = True
        for language in SUPPORTED_LANGUAGES:
            self.locale_dir.joinpath(language, 'LC_MESSAGES').mkdir(parents=True, exist_ok=True)
            updated_catalog = self._get_updated_translations(language, new_catalog)
            is_complete = is_complete and self._is_translations_complete(updated_catalog, language)
            with self.locale_dir.joinpath(language, 'zordon.po').open(mode='wb') as file:
                pofile.write_po(file, updated_catalog, sort_output=True, width=None, omit_header=True)
            with self.locale_dir.joinpath(language, 'LC_MESSAGES', 'zordon.mo').open(mode='wb') as file:
                mofile.write_mo(file, updated_catalog)
        return is_complete

    def _build_strings_catalog_from_sources(self) -> catalog.Catalog:
        strings_dict = self._get_translatable_strings()
        result = catalog.Catalog()
        for msg, locations in strings_dict.items():
            result.add(msg, locations=locations,)
        return result

    def _get_translatable_strings(self) -> dict:
        strings_list = extract.extract_from_dir(dirname=str(self.sources_dir))
        strings_dict = {}
        for filename, line_num, msg, _, context in strings_list:
            if msg in strings_dict:
                strings_dict[msg].append((filename, line_num))
            else:
                strings_dict[msg] = [(filename, line_num)]
        return strings_dict

    def _get_updated_translations(self, language: str, new_catalog: catalog.Catalog) -> catalog.Catalog:
        current_catalog = self._read_existing_translations_for_language(language)
        current_catalog.update(new_catalog)
        if current_catalog.obsolete:
            obsolete_lines = ', '.join(current_catalog.obsolete.keys())
            logging.warning('Obsolete lines found in {lang}: {lines}'.format(lang=language, lines=obsolete_lines))
        catalog.fuzzy = False
        return current_catalog

    def _read_existing_translations_for_language(self, language: str) -> catalog.Catalog:
        file_path = Path(str(self.locale_dir.joinpath(language, 'zordon.po')))
        if file_path.is_file():
            with file_path.open(mode='rb') as file:
                return pofile.read_po(file, locale=language, domain='zordon')
        return catalog.Catalog()

    @staticmethod
    def _is_translations_complete(strings_catalog: catalog.Catalog, language: str) -> bool:
        is_translations_valid = True
        for msg in strings_catalog:
            if not msg.string:
                logging.error('Translation for {msg}({lang}) is missing!'.format(msg=msg.id, lang=language))
                is_translations_valid = False
            elif msg.check():
                errors = ', '.join(map(str, msg.check()))
                logging.error('{msg}({lang}): {errors}'.format(msg=msg.id, lang=language, errors=errors))
                is_translations_valid = False
        return is_translations_valid
