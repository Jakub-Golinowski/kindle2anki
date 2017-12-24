import importlib
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_dict_class(module_class):
    """
    Return the dictionary class 
    :param module_class: the name of module and class in the form of "module.class"
    :return: class object of the dictionary
    """

    class_ = None
    module_name, class_name = module_class.rsplit(".", 1)
    try:
        module_ = importlib.import_module(module_name)
        try:
            class_ = getattr(module_, class_name)
        except AttributeError:
            logging.error('Class does not exist: {}'.format(class_name))
    except ImportError:
        logging.error('Module does not exist: {}'.format(module_name))
    return class_


def test():
    HJDict = create_dict_class("hjdict.simple.HJDict_Simple")
    if HJDict is not None:
        my_dict = HJDict()
        res = my_dict.look_up("好き")
        print(res)


if __name__ == '__main__':
    test()
