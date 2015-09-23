#!/usr/bin/env python

from __future__ import print_function
import sys

def print_usage():
  print("""
Replaces custom vars from a file and echoes that file

Usage:
  %s file.svg var=val [var=val ...]
""" % sys.argv[0], file=sys.stderr)

def main():
  if len(sys.argv) < 2:
    print_usage()
    sys.exit(1)

  f = None
  content = None
  try:
    f = open(sys.argv[1], 'r')
    content = f.read()
  except IOError:
    print("IOError reading from %s, are you sure it exists?" % sys.argv[1], file=sys.stderr)
  finally:
    if f:
      f.close()

  for arg in sys.argv[2:]:
    key_and_val = arg.split('=', 1)
    key = arg
    val = arg

    if len(key_and_val) == 1:
      print("Warning: key passed without value, using the same key", file=sys.stderr)
    else:
      key = key_and_val[0]
      val = key_and_val[1]

    content = content.replace("{{%s}}" % key, val)

  print(content)

if __name__ == '__main__':
  main()
