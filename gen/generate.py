#!/usr/bin/env python

from __future__ import print_function
import re
import sys
import os
import subprocess

VOWELS = set('aeiou')

def pluralize(singular):
  if not singular:
    return ''

  root = singular

  try:
    if singular[-1] == 'y' and singular[-2] not in VOWELS:
      root = singular[:-1]
      suffix = 'ies'
    elif singular[-1] == 's':
      if singular[-2] in VOWELS:
        if singular[-3:] == 'ius':
          root = singular[:-2]
          suffix = 'i'
        else:
          root = singular[:-1]
          suffix = 'ses'
      else:
        suffix = 'es'
    elif singular[-2:] in ('ch', 'sh'):
      suffix = 'es'
    else:
      suffix = 's'
  except IndexError:
    suffix = 's'

  plural = root + suffix
  return plural

def dasherize(str):
  ret = re.sub(r"([A-Z])", "-\\1", str)
  if ret[0] == '-':
    ret = ret[1:]

  return ret.lower()

def underscoreize(str):
  return dasherize(str).replace('-', '_')

def humanize(str):
  return dasherize(str).replace('-', ' ')

REPLACER = '../scripts/generate-diagram.py'

def convert(file, actor, model, replacements):
  target_dir = 'target/{0}/{1}'.format(os.path.basename(file).split('.', 1)[0], actor)
  command = [ REPLACER, os.path.abspath(file)]

  for k, v in replacements.items():
    command.append("{0}={1}".format(k, v))

  try:
    os.makedirs(target_dir)
  except OSError:
    pass

  f = None
  p = None
  try:
    target_name = target_dir + '/%s.svg' % model
    if os.path.exists(target_name) and os.path.getmtime(target_name) >= os.path.getmtime(file):
      print("[CACHE] {0}".format(target_name))
    else:
      command_str = ' '.join(command)
      print("[GEN] {0}: {1}".format(target_name, command_str))
      f = open(target_name, 'w')
      p = subprocess.Popen(command, stdout=f, stderr=sys.stderr)
  except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror), file=sys.stdout)
    sys.exit(1)
  except OSError as e:
    print("OS error({0}): {1}".format(e.errno, e.strerror), file=sys.stdout)
    sys.exit(1)
  finally:
    if f:
      f.close()
    if p:
      p.wait()

def main():
  actors = []
  svgs = []
  models = []

  targets = [actors, svgs, models]
  current_target = 0
  target = svgs
  for arg in sys.argv[1:]:
    if arg == '--':
      current_target += 1
      continue

    targets[current_target].append(arg)

  for actor in actors:
    for svg in svgs:
      for model in models:
        convert(svg, actor, model, {
          'actor': actor,
          'model_name': model,
          'underscored_model_name': underscoreize(model),
          'plural_model_name': pluralize(model)
        })

if __name__ == '__main__':
  main()
