#!/usr/bin/env python

import os
import re
import fnmatch

#
# TODO: Make this suck less
#
# Right now this just prints the tables and you have to crop them
# by hand
#
# Is enough tough

OBJECTIVES_PATH = '../03-requisites/01-objectives'
REQUISITES_PATHS = {
  'information': '../03-requisites/02-information-requisites',
  'functional': '../03-requisites/03-functional-requisites',
  'nonfunctional': '../03-requisites/04-nonfunctional-requisites'
}

def find_all_tex_files(folder):
  matches = []
  for root, dirnames, filenames in os.walk(folder):
    for filename in fnmatch.filter(filenames, '*.tex'):
      matches.append(os.path.join(root, filename))

  return matches

def parse_object(tex_contents, object_type = 'OBJ'):
  matches = re.search('(objective|requisite)\[id=([0-9]+)', tex_contents)

  if not matches:
    return None

  id = matches.group(2);

  # This is fucking dumb and will break if we use the obj- string in
  # something that are not dependencies
  # TODO: The "good way" would be split the tex args and pick the corres-
  # ponding one
  related = re.findall('(OBJ|IRQ|NFR|FRQ)-([0-9]+)', tex_contents)

  return {
    'id': (object_type, id),
    'numeric_id': int(id),
    'related': related,
  }

def find_objects(path, type):
  for objective_file in find_all_tex_files(path):
    file = open(objective_file)
    obj = parse_object(file.read(), type)
    file.close()
    if obj:
      yield obj


def find_objectives():
  return find_objects(OBJECTIVES_PATH, 'OBJ')

def find_requisites():
  for obj in find_objects(REQUISITES_PATHS['information'], 'IRQ'):
    yield obj

  for obj in find_objects(REQUISITES_PATHS['functional'], 'FRQ'):
    yield obj

  for obj in find_objects(REQUISITES_PATHS['nonfunctional'], 'NFR'):
    yield obj

def print_objs_reqs_table(objectives, requisites):
  print('<table>')
  print('<thead>')
  print('<tr>')
  print('<th></th>')
  for obj in objectives:
    print('<th>' + '-'.join(obj['id']) + '</th>')
  print('</tr>')
  print('</thead>')
  print('<tbody>')
  for req in requisites:
    print('<tr>')
    print('<td>' + '-'.join(req['id']) + '</th>')
    for potential_sub in objectives:
      print('<td>')
      if potential_sub['id'] in req['related']:
        print('&times;')
      else:
        print('-')
      print('</td>')
    print('</tr>')
  print('</tbody>')
  print('</table>')

def print_reqs_reqs_table(requisites):
  print('<table>')
  print('<thead>')
  print('<tr>')
  print('<th></th>')
  for obj in requisites:
    print('<th>' + '-'.join(obj['id']) + '</th>')
  print('</tr>')
  print('</thead>')
  print('<tbody>')
  for req in requisites:
    print('<tr>')
    print('<td>' + '-'.join(req['id']) + '</th>')
    for potential_sub in requisites:
      print('<td>')
      if potential_sub['id'] in req['related']:
        print('&times;')
      else:
        print('-')
      print('</td>')
    print('</tr>')
  print('</tbody>')
  print('</table>')


def main():
  requisites = [req for req in find_requisites()]
  requisites = sorted(requisites, key = lambda obj: obj['id'])

  objectives = [obj for obj in find_objectives()]
  objectives = sorted(objectives, key = lambda obj: obj['numeric_id'])

  print_objs_reqs_table(objectives, requisites)
  print_reqs_reqs_table(requisites)
if __name__ == '__main__':
  main()
