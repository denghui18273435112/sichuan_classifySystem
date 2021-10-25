#
# import yaml
# import os.path
# class Loader(yaml.Loader):
#     def __init__(se1f,stream) :
#         se1f._root = os.path.split(stream.name)[0]super(Loader， se1f)._init_(stream)
#     def include(self，node):
#         filename = os.path.join(self._root,se1f.construct_scalar(node))
#     with open(filename，'r') as f:
#     return yam1 .1oad(f，Loader)
# Loader.add_constructor( ' !include ', Loader.include)
