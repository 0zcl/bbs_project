from django.test import TestCase
import json
# Create your tests here.

a = ""
if not a:
    print("aa")


def func():
    test_list = []
    return json.dumps(test_list)

test = func()
print(">>", test)
