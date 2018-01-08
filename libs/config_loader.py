import platform
import sys
import configargparse
import logging
import os


def load_config():
    cur_dir = os.path.dirname(__file__)
    config_dir = os.path.join(cur_dir, os.pardir, 'config')
    overall_default = os.path.join(config_dir, 'config.default.yml')
    pc_name = platform.node()
    pc_specific_config = os.path.join(config_dir, 'config.{pc_name}.yml'.format(pc_name=pc_name))

    default_configs = [overall_default, pc_specific_config]
    # print("Trying to load default config files:\n{0}".format("\n".join(default_configs)))

    parser = configargparse.ArgParser(default_config_files=default_configs)
    parser.add_argument(
        '-c',
        '--config',
        is_config_file=True, help='Config file path.')
    parser.add_argument(
        '--kindle', help='Path to kindle db file (usually vocab.db)')
    parser.add_argument(
        '--src', help='Path to "documents/My Clippings.txt" on kindle')
    parser.add_argument(
        '--anki-profile', help='Profile name of Anki.')
    parser.add_argument(
        '--collection', help='Path to anki collection file (.anki file)')
    parser.add_argument('--deck', help='Anki deck name.')
    parser.add_argument('--card-type', help='Anki card type to use.')
    parser.add_argument(
        '-o',
        '--out',
        help='CSV output filename to import into anki, if not provided words are added to provided Anki deck and collection')
    parser.add_argument(
        '-m',
        '--media-path',
        help='Where to store media files (sounds/images) from Lingualeo')
    parser.add_argument('--email', help='LinguaLeo account email/login')
    parser.add_argument(
        '--update-timestamp',
        help='Update local timestamp to now and exit',
        default=False,
        action="store_true")
    parser.add_argument('--pwd', help='LinguaLeo account password')
    parser.add_argument(
        '--max-length',
        help='Maximum length of words from clippings, to avoid importing big sentences',
        default=30)
    parser.add_argument(
        '--verbose',
        help='Show debug messages',
        default=False,
        action="store_true")
    parser.add_argument(
        '--no-ask',
        help='Do not ask for card back in the command line',
        default=False,
        action="store_true")
    parser.add_argument(
        '--clipboard',
        help='Copy each word to clipboard',
        default=False,
        action="store_true")
    parser.add_argument(
        '--lang-dict',
        help='(lang, dict) pair.',
        action="append"
    )
    parser.add_argument(
        '--tags',
        help='A list of tags to add to notes.',
        action="append"
    )
    parser.add_argument(
        '--traditional-chinese',
        default=False,
        help='Convert simplified Chinese to traditional Chinese.',
        action="store_true"
    )

    config = parser.parse_args()

    if not config.collection:
        config.collection = construct_collection_path(config)

    if config.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    config.config_dir = config_dir

    logging.info("------------------------------------")
    logging.info(parser.format_values())
    logging.info("------------------------------------")

    return config


def construct_collection_path(args):
    isMac = sys.platform.startswith("darwin")
    isWin = sys.platform.startswith("win32")
    if isWin:
        path_temp = os.path.expanduser("~\AppData\Roaming\Anki2\{anki_profile}\collection.anki2")
    elif isMac:
        path_temp = os.path.expanduser("~/Library/Application Support/Anki2/{anki_profile}/collection.anki2")
    else:
        # TODO: check on linux
        path_temp = os.path.expanduser("~/Anki/{anki_profile}/collection.anki2")

    col_path = path_temp.format(anki_profile=args.anki_profile)
    # print(col_path)
    return col_path


def test():
    logging.getLogger().setLevel(logging.DEBUG)
    load_config()


if __name__ == '__main__':
    test()