import subprocess

class Task(object):
    _task_counter = 0

    def __init__(self, command, mode="sync"):
        Task._task_counter += 1
        self.task_id = Task._task_counter
        self.command = command
        self.mode = mode  # "sync" or "async"
        self.process = None
        self.result = None
        self.stdout_iterator = None

    def start(self):
        if self.mode == "sync":
            self._run_sync_task()
        elif self.mode == "async":
            self._start_async_task()

    def _run_sync_task(self):
        self.result = subprocess.run(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=True,
            check=True
        )

    def _start_async_task(self):
        self.process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=True
        )

    def is_running(self):
        if self.mode == "async":
            status = self.process and self.process.poll() is None
            return status
        else:
            return False

    def get_sync_output(self):
        return self.result.stdout.splitlines()

    def get_async_output(self):
        # while self.is_running(): # only for cmd `watch`
        #     yield stdio.read(1)
        while self.is_running():
            yield self.process.stdout.readline()

    def get_output(self, io="stdout"):
        if self.mode == "sync":
            return self.get_sync_output()
        elif self.mode == "async":
            return self.get_async_output()
        else:
            print("Wrong mode!")

    def stop(self):
        if self.mode == "sync":
            print(f"[Task {self.task_id}] Sync task cannot be stopped.")
            return False
        elif self.mode == "async":
            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait()
                print(f"[Task {self.task_id}] Task has been terminated.")
                return True
            else:
                print(f"[Task {self.task_id}] Task is already finished.")
                return False

class JupyterTunnel(object):
    def __init__(self):
        self.url = "https://github.com/cloudflare/cloudflared/releases/download/2025.2.0/cloudflared-linux-amd64"
        self.bin = "/usr/local/bin/cloudflared"
        self.tunnel = None

    def init(self):
        task = Task(f"wget {self.url} -O {self.bin} && chmod a+x {self.bin}")
        task.start()
        for msg in task.get_output():
            print(msg, flush=True)

    def start(self, port=12345, print_lines=15):
        self.tunnel = Task(f"stdbuf -oL -eL cloudflared tunnel --url http://127.0.0.1:{port}", mode="async")
        self.tunnel.start()
        iter = 0
        for msg in self.tunnel.get_output():
            iter += 1
            print(msg, flush=True)
            if iter > print_lines:
                break

    def stop(self):
        if self.tunnel:
            self.tunnel.stop()
