import platform
import sys
import configargparse
import logging
import os



def load_config():
    cur_dir = os.path.dirname(__file__)
    config_dir = os.path.join(cur_dir, os.pardir, 'config')
    default_config_file = os.path.join(config_dir, 'config.default.yml')
    pc_name = platform.node()
    default_config_file_pc = os.path.join(config_dir, 'config.{pc_name}.yml'.format(pc_name=pc_name))
    # print(default_config_file_pc)

    parser = configargparse.ArgParser(default_config_files=[default_config_file, default_config_file_pc])
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
    parser.add_argument('--deck', help='Anki deck name')
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

    args = parser.parse_args()

    if not args.collection:
        args.collection = construct_collection_path(args)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.info("------------------------------------")
    logging.info(parser.format_values())
    logging.info("------------------------------------")

    return args


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
    load_config()


if __name__ == '__main__':
    test()