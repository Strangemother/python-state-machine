import os, binascii, inspect

def random_string(count=6):
    return binascii.b2a_hex(os.urandom(count))

def overload(o, s, v, pushing=False, push_branch='__pushed'):
    ''' Push support moves an existing
    branch to a new node before an object is written
    called __push '''
    split = s.split('.')
    obj = o
    count = len(split)
    i = 0
    made = False;
    for x in split:
        i += 1

        xs = str(x)
        #print 'looking at', xs, 'in', o
        if x in obj and made is False:
            #print x, 'in object'
            # Thats good. we go into that to search the next child.
            #if isinstance(obj[xs],object):
            if hasattr(obj[xs], '__iter__') and isinstance(obj[xs],object):
                if i == count:
                    #print 'Writing new value', v
                    obj[xs] = v
                else:
                    obj = obj[xs]
            else:
                # we've reached the end of the line and
                # anything beyond this is scrapped
                # or overloaded.
                # In this case, we rewrite the current object
                # print "Hit", type(obj[xs])
                d = obj[xs]
                if pushing:
                    obj[xs] = { push_branch: d}
                else:
                    obj[xs] = d
                obj = obj[xs]
        else:
            #print 'making', x
            # nope. We make that node.
            obj[xs] = {}

            made = True;

            if count == i:
                # last Item in list is given a value.
                obj[xs] = {}
                obj[xs] = v
                #print 'gave', x, 'value of ', v
            else:
                #print 'step into', x
                obj = obj[xs]
    return obj
