class Node:
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def pprint(self, indent):
        print(indent*'\t' + repr(self))
        for k, i in vars(self).items():
            if isinstance(i, Node):
                i.pprint(indent + 1)
            elif isinstance(i, list):
                print(indent*'\t'+"[")
                for j in i:
                    if isinstance(j, Node):
                        j.pprint(indent + 1)
                    else:
                        print(indent*'\t'+repr(j))
                print(indent*'\t'+"]")


