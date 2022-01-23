
# distrilockper - Distributed Lock Helper

### Feature
- Support Redis Cluster and Redis Single setup
- Redis operation with Lua scripting (Atomic operations)
- Lock watch dog (auto increase the alive time of key if the process time is large than key ttl)
- Thread safe
- Support Reentrant lock
- Support expired unlock function, automatically unlock after x seconds, no need to manually unlock by call unlock method
- Support try lock, wait n second if the lock is existed.

### Basic Usage

1. Install 

    ```python
    pip install distrilockper
    ```

2. declare config instance

    ```python
    from distrilockper import Config
    config = Config()
    ```

3. select single Redis server mode or cluster Redis servers mode

    ```python
    config.use_single_server()

    ```

    ```python
    config.use_cluster_servers()
    ```

4. set the config

    ```python
    config.use_single_server().set_config(host='0.0.0.0', port=6379)
    ```

    ```python
    config.use_cluster_servers().set_config(host='0.0.0.0', port=7000)
    ```

    ```python
    config.use_cluster_servers().add_node_address(host='0.0.0.0', port=7000) \
                                    .add_node_address(host='0.0.0.0', port=7001) \
                                    .add_node_address(host='0.0.0.0', port=7002) \
                                    .add_node_address(host='0.0.0.0', port=7003) \
                                    .add_node_address(host='0.0.0.0', port=7004) \
                                    .add_node_address(host='0.0.0.0', port=7005)
    ```

    The set_config and add_node_address method takes several arguments from python redis library

5. declare the lock instance

    ```python
    helper = LockHelper()
    helper.create(config)
    ```

6. get a kind of lock

    ```python
    lock = helper.get_reentrant_lock(key='apples')
    ```

7. try lock the key

    ```python
    result = lock.try_lock(wait_time=10,lease_time=7,time_unit='second')
    ```

    The try_lock method takes several arguments:

    - `wait_time` : try lock operation time out
    - `lease_time` : the release time of the lock
    - `time_unit` : unit of lease_time and wait_time
        - `seconds` / `s`
        - `hour` / `h`
        - `minute` / `m`
        - `milliseconds`/ `ms`

8. unlock after business logic done

    ```python
    lock.unlock()
    ```

## Reentrant

the reentrant lock only support in the same thread

### Get the lock in different thread

```python
from distrilockper import Config
from distrilockper import LockHelper
from multiprocessing.dummy import Pool as ThreadPool

config = Config()
config.use_single_server().set_config(host='0.0.0.0', port=6379)

helper = LockHelper()
helper.create(config)

def get_lock(_):
    print("run", _)
    Locker1 = helper.get_reentrant_lock(key='apples')
    re1 = Locker1.try_lock(60, 10, 'second')
    assert re1 == True
    print("get lock",re1)
    assert Locker1.is_exists() == True
    print('exists', Locker1.is_exists())

pool = ThreadPool(100)
results = pool.map(get_lock, range(10))
```

### get the lock in same thread

```python
from distrilockper import Config
from distrilockper import LockHelper
from multiprocessing.dummy import Pool as ThreadPool

config = Config()
config.use_single_server().set_config(host='0.0.0.0', port=6379)

helper = LockHelper()
helper.create(config)

for i in range(10):
    Locker1 = helper.get_reentrant_lock(key='apples')
    re1 = Locker1.try_lock(60, 10, 'second')
    assert re1 == True
    print("get lock", re1)
    assert Locker1.is_exists() == True
    print('exists', Locker1.is_exists())
```
