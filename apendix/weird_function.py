# weird_function.py
# 
# Create function that will have next result:
#     print(super_weird_sum(5)())           -> 5
#     print(super_weird_sum(5)(3)())        -> 8
#     print(super_weird_sum(5)(4)(-10)())   -> -1

def super_weird_sum(value):
    inner_lst = [value]

    def inner_fun(*args):
        if args:
            inner_lst.append(args[0])
            return inner_fun
        else:
            return sum(inner_lst)
    return inner_fun    


if __name__ == "__main__":
    print(f"super_weird_sum(5)() = {super_weird_sum(5)()}")
    print(f"super_weird_sum(5)(3)() = {super_weird_sum(5)(3)()}")
    print(f"super_weird_sum(5)(4)(-10)() = {super_weird_sum(5)(4)(-10)()}")
    print(f"super_weird_sum(5)(4)(-10)(11)() = "
          f"{super_weird_sum(5)(4)(-10)(11)()}")

    assert super_weird_sum(5)() == 5, "super_weird_sum(5)() must be the 5"
    assert super_weird_sum(5)(3)() == 8, \
        "super_weird_sum(5)(3)()} must be the 8"
    assert super_weird_sum(5)(4)(-10)() == -1, \
        "super_weird_sum(5)(4)(-10)() must be the -1"
    assert super_weird_sum(5)(4)(-10)(11)() == 10, \
        "super_weird_sum(5)(4)(-10)(11)()} must be the 10"
