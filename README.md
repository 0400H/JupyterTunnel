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

Start:

```
from jupytertunnel import JupyterTunnel, Task

tunnel = JupyterTunnel()
tunnel.init() # download cloudflared

tunnel.start(port=12345) # your service port
```

Get URL from output:

```
Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):

https://xxxxxxxxxxxxxxxxxxx.trycloudflare.com
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

3\. Use tunnel via URL

User can use this tunnel via `URL`.

4\. Stop tunnel

```
tunnel.stop()
```
