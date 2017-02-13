Context Managers
================

The `with` statement
--------------------
The `with` statement is used to wrap the execution of a block of code with methods defined by a context manager. It sets up a temporary context around the code you want to execute and reliably tears it down. This allows common `try...except...finally` patterns to be encapsulated to reduce boilerplate code and prevent errors. One of the most common usage is to automatically close a file:

```python
with open('file.txt', 'r') as fp:
    print(fp.readline())
```
After that the code within the `with` block has been executed, the context manager closes the file.
The general usage of the `with` statement is shown by the following pseudocode snippet:

```python
with expression as target: # target is optional
    code_block
```

The execution of the code above proceeds as follows (taken from [*The Python Language Reference*](https://docs.python.org/3.6/reference/compound_stmts.html#the-with-statement)):  
 1. the context expression (`expression`) is evaluated to obtain a context manager object
 2. the context managers's `__exit__()` method is loaded for later use
 3. the context manager's `__enter__()` is invoked
 4. if a `target` is provided, then the return value of the manager's `__enter__()` method is assigned to it
 5. the code block is executed
 6. the context manager's `__exit__()` method is invoked; if an exception caused the code block to be exited, its type, value and traceback are passed as arguments to `__exit__()`, otherwise three `None` arguments are supplied.

Note that the `target` is optional and its actual value depends on the returned value of the manager's `__enter__()` method. In case of `open()`, the target is bound to the opened file because the file's `__enter__()` method returns `self`.
The `with` statement guarantees that if the `__enter__()` method returns without an error, then `__exit__()` will always be called. If an error occurs during the assignment to the target list, it will be treated as it would be occurred within the internal code block, supplying the exception type, values and traceback as arguments of `__exit__()`.

ContextManager objects
----------------------
The [context manager protocol](https://docs.python.org/3.6/library/stdtypes.html#typecontextmanager) is implemented by two methods, `__enter__` and `__exit__`:

####`contextmanager.__enter__()`
Enter the runtime context. The value returned by this method is bound to the identifier in the `as` clause of `with` statements. This method usually returns the same context manager, such as file objects, or another objects related to the runtime context. For instance, `decimal.localcontext()` returns a copy of the original decimal context.

####`contextmanager.__exit__(exc_type, exc_val, exc_tb)`
Exit the runtime context and return a Boolean flag. This flag indicates if any exception that occurred during the execution of the body of the `with` statement should be suppressed: if a `True` value is returned, then the `with` statement will suppress the occurred exception and continue the execution of the program, otherwise it will be propagated after the execution of this method. If an exception occurred during the execution of the `with` boby, the arguments contain the exception type, value and traceback information.

Let's define a dummy context manager:

```python
class DummyContextManager:
    
    def __init__(self):
        self.status = 'inactive'
    
    def __enter__(self):
        print('I\'m entering the context')
        self.status = 'active'
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('I\'m leaving the context')
        if exc_type:
            print('An exception of type {} has occurred with value "{}"'.format(
                exc_type, exc_val))
        self.status = 'inactive'
```

When used in a `with` statement, it produces the following output:
```
>>> with DummyContextManager() as cm:
...     print('The context is now ' + cm.status)
I'm entering the context
The context is now active
I'm leaving the context
>>> print('The context is now ' + cm.status)
The context is now inactive
```
If an exception occurs inside the context, i.e. after that the `__enter__` method has sucessfully returned, its type, value and traceback are passed as arguments to the `__exit__` method. Furthermore, since the (implicit) value returned by `__exit__` is `None`, the exception will be propagated outside the context.
```
>>> with DummyContextManager():
...     raise Exception('I\'m an exception')
I'm entering the context
I'm leaving the context
An exception of type <class 'Exception'> has occurred with value "I'm an exception"
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
Exception: I'm an exception
```
To prevent an exception to be propagated outside the context, we have to make the `__exit__` method return `True`.
```python
class ValueErrorContextManager(DummyContextManager):
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        if exc_type is ValueError:
            print('This exception has been successfully handled!')
            return True
```
Now, if a `ValueError` is raised inside the context it will be handled by the context manager's `__exit__` method and not propagated.
```
>>> with ValueErrorContextManager() as cm:
...     raise ValueError('ooops...')
I'm entering the context
I'm leaving the context
An exception of type <class 'ValueError'> has occurred with value "ooops..."
This exception has been successfully handled!
```
