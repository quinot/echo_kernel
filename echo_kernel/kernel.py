from ipykernel.kernelbase import Kernel
import re
import time

wait_re = re.compile("wait (\d+)")


class EchoKernel(Kernel):
    implementation = 'Echo'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Echo kernel - as useful as a parrot, on steroids"

    def init_metadata(self, parent):
        self.m = super(EchoKernel, self).init_metadata(parent)
        self.m["parent"] = parent
        return self.m

    def do_execute(self, code, silent,
                   store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout', 'text': code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

            stream_content = {'name': 'stdout', 'text': "\nmetadata was %s" % self.m}
            self.send_response(self.iopub_socket, 'stream', stream_content)

            m = wait_re.search(code)
            if m:
                time.sleep(int(m.group(1)))
                stream_content = {'name': 'stdout', 'text': "waited %d" % m.group(1)}


        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}}
