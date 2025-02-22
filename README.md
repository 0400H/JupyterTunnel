# JupyterTunnel

Enable Cloudflare port forwarding on jupyter.

### Cloud Test Status

|Cloud|Status|
|--|--|
|Google Colab|Pass|

### How to Install

```
pip install git+https://github.com/0400H/JupyterTunnel.git
```

### How to use it

1\. Start tunnel

```
from jupytertunnel import JupyterTunnel, Task

tunnel = JupyterTunnel()
tunnel.init() # download cloudflared

tunnel.start(port=12345) # your service port
```

get url from output:

```

```

2\. Start service

- start at foreground

    ```
    !python -u -m http.server 12345
    ```

- start at background

    ```
    task = Task("python -u -m http.server 12345", mode="async")
    task.start()

    iter = 0
    for msg in task.get_output():
        iter += 1
        print(msg, flush=True)
        if iter > 5:
            break
    ```

3\. Stop tunnel

```
tunnel.stop()
```