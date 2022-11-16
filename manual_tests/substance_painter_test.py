import generic


def start_plugin():
    generic.create_test_menus()
    # todo currently runs into c++ issues. as soon as we parent the menu to the buildin UI (c++)
    # the python var gets garbage collected and any further parenting wont work.
    # this does work correctly when loaded from a config though
